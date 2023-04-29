# coding: utf-8
import json
import requests
import time

from flask import Blueprint, request, render_template, session, g, Response, send_from_directory
from middleware import access_verify
from models.user import User
from models.word import Word,Collections, UserLearnedWords, Topic, TopicWord, UserTopic
from services import user_has_learned_this_word, user_learned_words_paged, user_collected_words_paged, user_learned_chinese_words_paged


bp = Blueprint("word", __name__)


@bp.route("/units")
@access_verify
def units():
    if request.method == 'GET':
        result = []
        ws = Word.query.distinct("unit").all()
        unit_list = [w.unit for w in ws]
        for unit in unit_list:
            total = Word.query.filter(Word.unit == unit).count()
            learned_count = UserLearnedWords.query.join(Word, UserLearnedWords.word_id == Word.id).filter(
                Word.unit == unit, UserLearnedWords.user_id == session.get("current_user_id")).count()
            result.append({
                "name": unit,
                "learned_count": learned_count,
                "total": total
            })
        print "------result", result
        return render_template("units.html", result=result)


@bp.route("/export/words")
@access_verify
def export_words():
    if request.method == 'GET':
        collections = Collections.query.filter().all()
        word_ids = [c.word_id for c in collections]
        words = Word.query.filter(Word.id.in_(word_ids))
        result = '&**&'.join(['%s(%s)'%(w.spell, w.meaning) for w in words])
        return Response(result)


@bp.route("/<unit>/")
@access_verify
def words_of_unit(unit):
    if request.method == 'GET':
        unLearned = request.args.get("unLearned", None)
        page = int(request.args.get("page", 1))
        page_size = 20

        if not unLearned:
            word_list = Word.query.filter(Word.unit == unit).limit(page_size).offset((page-1)*page_size)
            total = Word.query.filter(Word.unit == unit).count()
        else:
            learned_word_with_ids = UserLearnedWords.query.filter(UserLearnedWords.user_id == session.get("current_user_id")).with_entities(UserLearnedWords.word_id).all()
            learned_word_ids = [x[0] for x in learned_word_with_ids]
            # print "------learned_word_ids:", learned_word_ids
            word_list = Word.query.filter(Word.unit == unit).filter(Word.id.notin_(learned_word_ids)).limit(page_size).offset((page-1)*page_size)
            total = Word.query.filter(Word.unit == unit).filter(Word.id.notin_(learned_word_ids)).count()

        for word in word_list:
            word.learned = user_has_learned_this_word(user_id=session.get("current_user_id"), word_id=word.id)
        return render_template("words.html", word_list=word_list, total=total,
                               pageSize=page_size, page=page, page_nums=range(1, (total / page_size) + 2))


@bp.route("/userLearned/<int:page_num>/")
@access_verify
def user_learned_words(page_num):
    if request.method == 'GET':
        total, page_count, word_list = user_learned_words_paged(user_id=session.get("current_user_id"), page_num=page_num)

        return render_template("wordsUserLearned.html",
                                word_list=word_list,
                                page_counts = range(1, page_count + 1),
                                page_num = page_num,
                                total = total
                               )

@bp.route("/chineseWordsUserLearned/<int:page_num>/")
@access_verify
def user_learned_chinese_words(page_num):
    if request.method == 'GET':
        total, page_count, word_list = user_learned_chinese_words_paged(user_id=session.get("current_user_id"), page_num=page_num)

        return render_template("chineseWordsUserLearned.html",
                                word_list=word_list,
                                page_counts = range(1, page_count + 1),
                                page_num = page_num,
                                total = total
                               )



@bp.route("/userCollected/<int:page_num>/")
@access_verify
def user_collected_words(page_num):
    if request.method == 'GET':
        total, page_count, word_list = user_collected_words_paged(user_id=session.get("current_user_id"), page_num=page_num)
        return render_template("wordsUserCollected.html",
                               word_list=word_list,
                               page_counts=range(1, page_count+1),
                               page_num=page_num,
                               total=total
                               )


@bp.route("/search/")
@access_verify
def search():
    if request.method == 'GET':
        word = request.args.get("word", "")
        if word:
            words = Word.query.filter(Word.spell.like("%" + word + "%"))
            return json.dumps([('%s'%w.spell, '%s'%w.soramimi) for w in words])


@bp.route("/sound/")
def sound():
    if request.method == 'GET':
        word = request.args.get("word", "")
        if word:
            import os
            if not os.path.exists("/tmp/%s.mp3"%word):
                w = requests.get("https://fanyi.baidu.com/gettts?lan=uk&text=%s&spd=3&source=web"%word)
                with open("/tmp/%s.mp3"%word,"wb") as code:
                    code.write(w.content)

        def generate():
            with open("/tmp/%s.mp3"%word, "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
        return Response(generate(), mimetype="audio/mpeg")


@bp.route("/topics/")
@access_verify
def topics():
    #topics = Topic.query.with_entities(Topic.name).distinct().all()
    user_topic_list = UserTopic.query.filter(UserTopic.user_id == session.get("current_user_id"))
    topics = Topic.query.filter(Topic.id.in_([x.topic_id for x in user_topic_list])).all()
    return render_template("topicList.html", topics=topics)


@bp.route("/wordsOfTopic/<topic_id>/")
def words_of_topic(topic_id):
    if request.method == 'GET':
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 20))
        download_audio = request.args.get("download_audio", None)

        topic_word_list = TopicWord.query.filter(TopicWord.topic_id == topic_id).limit(page_size).offset((page-1)*page_size)
        words = Word.query.filter(Word.id.in_([x.word_id for x in topic_word_list])).all()

        file_name = 'words_%s.mp3'%str(int(time.time()))
        file_path = '/tmp/' + file_name
        if download_audio:
            file = open(file_path, 'ab')

            for word in words:
                res = requests.get('https://fanyi.baidu.com/gettts?lan=uk&text=%s&spd=3&source=web' % word.spell)
                file.write(res.content)
            file.flush()
            return send_from_directory('/tmp/', file_name, as_attachment=True)
        return render_template("wordsOfTopic.html", words=words)
