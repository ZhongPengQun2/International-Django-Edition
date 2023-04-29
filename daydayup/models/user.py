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


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, comment=u"用户名")
    password = db.Column(db.String(200), comment=u"密码")
    current_topic = db.Column(db.String(200), comment=u"currently learning topic")

    def __repr__(self):
        return '<User %r>' % self.username
