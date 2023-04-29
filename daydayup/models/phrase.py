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


class Phrase(Base):
    __tablename__ = "phrases"
    id = db.Column(db.Integer, primary_key=True)
    spell = db.Column(db.String(200), unique=True, comment=u"spell")
    meaning = db.Column(db.String(500), comment=u"meaning")

    def __repr__(self):
        return '<Phrase %r>' % self.spell


