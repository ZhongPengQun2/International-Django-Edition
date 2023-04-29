# # coding: utf-8
#
# # The examples in this file come from the Flask-SQLAlchemy documentation
# # For more information take a look at:
# # http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships
# from database import db
# from sqlalchemy import UniqueConstraint, ForeignKey, CheckConstraint
# from database.models import Base
#
from models import db
from sqlalchemy import ForeignKey
from models.base import Base
import datetime


class Topic(Base):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(800), unique=True, comment=u"name")    


class UserTopic(Base):
    __tablename__ = "user_topic"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)


class Word(Base):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    spell = db.Column(db.String(800), unique=True, comment=u"spell")
    pronunciation = db.Column(db.String(800), comment=u"pronunciation")
    unit = db.Column(db.String(800), comment=u"unit")
    meaning = db.Column(db.String(800), comment=u"meaning")
    speak = db.Column(db.String(800), comment=u"speak")     # 发音的音频
    soramimi = db.Column(db.String(800), comment=u"soramimi")    # 空耳
    short_meaning = db.Column(db.String(800), comment=u"short_meaning")
    

class TopicWord(Base):
    __tablename__ = "topic_words"
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)


class UserLearnedWords(Base):
    __tablename__ = "user_learned_words"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)

    def __repr__(self):
        return '<UserLearnedWords %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Collections(Base):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Collections %r>' % self.id


class ChineseWord(Base):
    __tablename__ = "chinese_word"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(800), comment=u"text of chinese word")

    def __repr__(self):
        return '<ChineseWord %r>' % self.id


class UserLearnedChineseWords(Base):
    __tablename__ = "user_learned_chinese_words"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    cn_word_id = db.Column(db.Integer)

    def __repr__(self):
        return '<UserLearnedChineseWords %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
