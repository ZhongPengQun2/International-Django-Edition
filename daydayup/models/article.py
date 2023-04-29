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


class Article(Base):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(800), comment=u"title")
    content = db.Column(db.Text, comment=u"content")
    video_embed_link = db.Column(db.String(800), comment=u"embed src link if this article has relevant video.")

    def __repr__(self):
        return '<Article %r>' % self.id
