# coding: utf-8
from flask import Blueprint, request, render_template, session, g, redirect
from middleware import access_verify
from models.user import User
from models.word import Word, UserLearnedWords, Collections, TopicWord, Topic
from models.article import Article
from services import user_has_learned_this_word, user_learned_words_paged, user_collected_words_paged, \
    add_a_word_to_db, get_a_word_detail
import re
import requests
import collections
import string

bp = Blueprint("api", __name__)


@bp.route("/text_analyse", methods=['GET', 'POST'])
#@access_verify
def text_analyse():
    if request.method == 'POST':
        text = request.form.get("text", '')
        user_id = request.form.get("user_id", None)
        if not user_id:
            return 'user_id required!'
        words = re.findall(r'[a-zA-Z]+|[%s]|\s|\d+' % string.punctuation, text)       # \s 空格. 把文章split成一个一个的元素，这些元素为--单词、标点符号、空格、顿号
        total, page_num, user_learned_words = user_learned_words_paged(user_id=user_id, page_size=1000000000)
        user_learned_words_spell = [x.spell.lower() for x in user_learned_words]
        unlearned_words = []
        for w in words:
            if w.lower() not in user_learned_words_spell:
                unlearned_words.append(w.lower())
        return 'Unlearned words:\n' + '\n'.join(unlearned_words)
        
