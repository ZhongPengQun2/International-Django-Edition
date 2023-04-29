# coding: utf-8
from flask import Blueprint, request, render_template, session, g, redirect, send_file, send_from_directory
from middleware import access_verify
from models.user import User
from models.word import Word, UserLearnedWords, Collections, TopicWord, Topic
from models.article import Article
from services import user_has_learned_this_word, user_learned_words_paged, user_collected_words_paged, \
    add_a_word_to_db, get_a_word_detail, translate_english_to_chinese
import re
import time
import copy
import requests
import collections
import string
import json
import services

bp = Blueprint("article", __name__)


@bp.route("/add", methods=['GET', 'POST'])
@access_verify
def article_add():
    if request.method == 'GET':
        return render_template("article_add.html")
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        video_embed_link = request.form.get("video_embed_link", "")

        article = Article(user_id=session.get("current_user_id"), title=title, content=content, video_embed_link=video_embed_link)
        article.save()

        words_extracted = re.findall(r'[a-zA-Z]+', content)
        for word in words_extracted:
            if not Word.query.filter(Word.spell == word).one_or_none():
                r = requests.get("https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&q=%s" % word)
                try:
                    result = r.json()
                except:
                    result = {}
                add_a_word_to_db(
                    spell=word,
                    pronunciation=result.get("basic", {}).get("uk-phonetic", u""),
                    meaning=u"\n".join(result.get("basic", {}).get("explains", u"")),
                    short_meaning=u"\n".join(result.get("translation", [])),
                    unit=u"文章中的"
                )
        return redirect('/article/list')


@bp.route("/list")
@access_verify
def article_list():
    if request.method == 'GET':
        articles = Article.query.filter(Article.user_id==session.get("current_user_id")).order_by(Article.id).all()
        return render_template("article_list.html", articles=articles)


@bp.route("/detail/<int:article_id>")
@access_verify
def article_detail(article_id):
    if request.method == 'GET':
        download_article = request.args.get("download_article", None)
        total, page_num, user_learned_words = user_learned_words_paged(user_id=session.get("current_user_id"), page_size=1000000000)
        user_learned_words_spell = [x.spell.lower() for x in user_learned_words]

        article = Article.query.filter(Article.id == article_id).one()
        words = re.split('[%s\s]' % string.punctuation, article.content.strip())        # 这篇文章中的所有单词
        all_unlearned_words = [x.lower().strip() for x in words if len(x) > 1 and x.lower().strip() not in user_learned_words_spell and not x.lower().strip().isdigit()]
        unlearned_word_2_count = collections.Counter(all_unlearned_words)
        unlearned_word_2_count_sorted = sorted(unlearned_word_2_count.items(), key=lambda d: d[1], reverse=True)

        # article.content = article.content.replace('\n', '<br>')
        # split_words = article.content.split(u' ')
        # article.content = u' '.join([u'<a>%s</a>'%x if x.lower() in unlearned_word_2_count.keys() else x for x in split_words])

        content_items = re.findall(r'[a-zA-Z]+|[%s]|\s|\d+' % string.punctuation, article.content)       # \s 空格. 把文章split成一个一个的元素，这些元素为--单词、标点符号、空格、顿号
        line_break_punctuations = ['.', '!', '?']
        temp_content_items = []
        for content_item in content_items:
            soramimi = get_a_word_detail(spell=content_item.lower()).soramimi
            if soramimi:
                temp_content_items.extend([content_item, '<a style="text-decoration:underline;">__%s__</a>'%soramimi])
            else:
                temp_content_items.append(content_item)
        
        content_items = temp_content_items
        content_items = ['%s<br>'%x if x in line_break_punctuations else x for x in content_items]
        
        article.content = u''.join([u'<a %s>%s(%s)</a>' % ('onclick=""' if get_a_word_detail(spell=x.lower()).short_meaning else '', x, get_a_word_detail(spell=x.lower()).short_meaning) if x.lower() in unlearned_word_2_count.keys() else x for x in content_items])
        article.content = '<br><br>' + article.content

        if download_article:
            file_path = '/tmp/article_%s.txt'%str(time.time())
            with open(file_path, 'w') as f:
                p = re.compile(r'<.*?>')
                content = copy.deepcopy(article.content)
                content = p.sub('__', content)
                content = content.replace('\n', '')
                f.write(content.encode('utf-8'))
            return send_file(file_path, as_attachment=True)

        unlearned_word_result = []
        for unlearned_word_item in unlearned_word_2_count_sorted:
            #unlearned_word_result.append([unlearned_word_item[0], unlearned_word_item[1], get_a_word_detail(spell=unlearned_word_item[0]).soramimi])
            passed = False
            collected = False
            currented = False
            word = Word.query.filter(Word.spell==unlearned_word_item[0]).one_or_none()
            if word:
                passed = bool(UserLearnedWords.query.filter(UserLearnedWords.user_id==session.get("current_user_id"), UserLearnedWords.word_id==word.id).first())
                collected = bool(Collections.query.filter(Collections.user_id==session.get("current_user_id"), Collections.word_id==word.id).first())
                current_user = User.query.filter(User.id==session.get("current_user_id")).one_or_none()
                topic = Topic.query.filter(Topic.name==current_user.current_topic).one_or_none()
                if topic:
                    currented = bool(TopicWord.query.filter(TopicWord.topic_id==topic.id, TopicWord.word_id==word.id).first())
            #print unlearned_word_item[0], unlearned_word_item[1], passed, collected, currented
            unlearned_word_result.append([unlearned_word_item[0], unlearned_word_item[1], get_a_word_detail(spell=unlearned_word_item[0]).soramimi, passed, collected, currented, get_a_word_detail(spell=unlearned_word_item[0]).meaning])
        return render_template("article_detail.html", article=article, words=unlearned_word_result)


@bp.route("/statistics", methods=['GET', 'POST'])
@access_verify
def article_statistics():
    if request.method == 'GET':
        return render_template("article_statistics.html")
    if request.method == 'POST':
        # TODO
        pass
# @bp.route("/stat/<int:article_id>")
# @access_verify
# def article_stat(article_id):
#     if request.method == 'GET':
#         article = Article.query.filter(Article.id == article_id).one()
#         words = re.split('[%s\s]' % string.punctuation, article.content.strip())
#         all_words = [x.lower().strip() for x in words if len(x) > 1]
#         word_2_count = collections.Counter(all_words)
#         words = sorted(word_2_count.items(), key=lambda d: d[1], reverse=True)
#         words_with_step = []
#         return render_template("article_detail.html", article=article, words=words)


@bp.route("/seize", methods=['POST'])
#@access_verify
def fragment_seize():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    if request.method == 'POST':
        # TODO
        sentence = request.form.get("sentence", '')
        sentence = sentence.replace(u".", u",")
        sentence_type = request.form.get("sentence_type", "")
        assert sentence_type in ['english', 'chinese']
        title = 'seize-the-inspire-%s'%sentence_type
        existed_article = Article.query.filter(Article.title == title).one_or_none()

        new_words = []
        content_items = re.findall(r'[a-zA-Z]+|[%s]|\s' % string.punctuation, sentence)      
        for word in content_items:
            if not Word.query.filter(Word.spell == word).first():
                chinese_meaning = services.translate_english_to_chinese(word)
                if not chinese_meaning:
                    continue
#                w = Word(spell=word, meaning=chinese_meaning)
#                w.save()
#                cn_meaning = Word.query.filter(Word.spell==word).first().meaning
#                new_words.append({word: cn_meaning})
                new_words.append({word: chinese_meaning})
        if not existed_article:
            article = Article(user_id=Article.query.filter().first().id, title=title, content=sentence)
            article.save()
        else:
            existed_article.content = existed_article.content + '.' + sentence
            existed_article.save()
        return json.dumps(new_words)


@bp.route("/evaluate/", methods=['GET', 'POST'])
def article_evaluate():
    if request.method == 'GET':
       return 'POST, user_id, content'
    if request.method == 'POST':
        user_id = request.form.get("user_id", None)
        content = request.form.get("content", "")
        if not user_id:
            return 'Please provide user_id!'
        total, page_num, user_learned_words = user_learned_words_paged(user_id=user_id, page_size=1000000000)
        user_learned_words_spell = [x.spell.lower() for x in user_learned_words]

        words = re.split('[%s\s]' % string.punctuation, content.strip())        # 这篇文章中的所有单词
        all_unlearned_words = [x.lower().strip() for x in words if len(x) > 1 and x.lower().strip() not in user_learned_words_spell and not x.lower().strip().isdigit()]
        return json.dumps(all_unlearned_words)
