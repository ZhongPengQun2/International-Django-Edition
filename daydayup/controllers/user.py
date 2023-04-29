# coding: utf-8
from flask import Blueprint, request, session, jsonify, render_template
from middleware import access_verify
from models.user import User
from models.word import UserLearnedWords, Collections, UserTopic, Word, Topic, TopicWord
from services import add_a_word_to_db

bp = Blueprint("user", __name__)


@bp.route("/hello")
@access_verify
def hello():
    if request.method == 'GET':
        users = User.query.all()
        print '------------------------x', users
        return 'xxx'


@bp.route("/info")
@access_verify
def user_info():
    if request.method == 'GET':
        user = User.query.filter(User.id == session.get('current_user_id')).one_or_none()
        topics = Topic.query.filter()
        return render_template('userInfo.html', user=user, topics=topics)


@bp.route("/updateCurrentTopic")
@access_verify
def update_current_topic():
    if request.method == 'GET':
        user = User.query.filter(User.id == session.get('current_user_id'))[0]
        user.current_topic = request.args.get("topic", "")
        user.save()
        if not Topic.query.filter(Topic.name == request.args.get("topic", "")).one_or_none():
            topic = Topic(name=request.args.get("topic", ""))    
            topic.save()
            user_topic = UserTopic(user_id=session.get('current_user_id'), topic_id=topic.id)
            user_topic.save()
        else:
            if not UserTopic.query.filter(UserTopic.user_id==user.id, UserTopic.topic_id==Topic.query.filter(Topic.name == request.args.get("topic", "")).one_or_none().id).one_or_none():
                user_topic = UserTopic(user_id=session.get('current_user_id'), topic_id=Topic.query.filter(Topic.name == request.args.get("topic", "")).one_or_none().id)
                user_topic.save()
        return jsonify({"error": "0"})


@bp.route("/passThisWord")
@access_verify
def pass_this_word():
    if request.method == 'GET':
        if request.args.get("word_id"):
            word_id = request.args.get("word_id")
            word = UserLearnedWords(word_id=word_id, user_id=session.get("current_user_id"))
            word.save()
            return jsonify({"error": "0"})

        elif request.args.get("word_spell"):
            word_spell = request.args.get("word_spell")
            _word = Word.query.filter(Word.spell == word_spell).one_or_none()
            if _word:
                w = UserLearnedWords(word_id=_word.id, user_id=session.get("current_user_id"))
                w.save()
                return jsonify({"error": "0"})
            else:
                word = add_a_word_to_db(spell=word_spell, unit=u'从文章来')
                w = UserLearnedWords(word_id=word.id, user_id=session.get("current_user_id"))
                w.save()
                return jsonify({"error": "0"})


@bp.route("/collectThisWord")
@access_verify
def collect_this_word():
    if request.method == 'GET':
        if request.args.get("word_spell", ""):
            if Word.query.filter(Word.spell == request.args.get("word_spell")).one_or_none():
                word_id = Word.query.filter(Word.spell == request.args.get("word_spell")).first().id
        else:
            word_id = request.args.get("word_id")
        word = Collections(word_id=word_id, user_id=session.get("current_user_id"))
        word.save()
        return jsonify({"error": "0"})


@bp.route("/tagThisWordAsCurrentTopic")
@access_verify
def tag_this_word_as_current_topic():
    if request.method == 'GET':
        if request.args.get("word_spell", ""):
            word = Word.query.filter(Word.spell == request.args.get("word_spell")).one_or_none()
            if word:
                word_id = word.id
            else:
                word = Word(spell=request.args.get("word_spell"))
                word.save()
                word_id = word.id
        else:
            word_id = request.args.get("word_id")
        
        current_user = User.query.filter(User.id == session.get('current_user_id'))[0]
        current_topic = Topic.query.filter(Topic.name == current_user.current_topic).one_or_none()
        if current_topic:
            topic_word = TopicWord(topic_id=current_topic.id, word_id=word_id)
            topic_word.save()
            return jsonify({"error": "0"})
        return jsonify({"error": "1"})

@bp.route("/soramimiThisWord")
@access_verify
def update_word_soramimi():
    if request.method == 'GET':
        if request.args.get("word_spell"):
            word_spell = request.args.get("word_spell")
            soramimi = request.args.get("soramimi")
            print '---------------word_spell:', word_spell
            _word = Word.query.filter(Word.spell == word_spell).one_or_none()
            print '---------------_word:', _word
            if _word:
                _word.soramimi = soramimi
                _word.save()
                print '------------soramimi:', soramimi
                return jsonify({"error": "0"})
