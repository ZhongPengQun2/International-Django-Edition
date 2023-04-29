# coding: utf-8
from datetime import datetime

from models import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self,  **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))

    def save(self):
        db.session.add(self)
        db.session.commit()