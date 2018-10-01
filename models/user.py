import sqlite3
from db import db

################################################
## model is internal representation of entity,##
################################################
"""
api doesn't return user so no need to add Resource
this class is not resource, just a helper for storing some data about users
and helper contain some methods that allow us retrieve user data from db

when we deal internally in our code with a User, for example, security.py
We're not using the resource, we're using the model
"""
class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id':self.id,
            'username': self.username
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
