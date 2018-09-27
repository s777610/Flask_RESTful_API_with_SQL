import sqlite3

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
class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)# row[0], row[1], row[2]
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)# row[0], row[1], row[2]
        else:
            user = None
        connection.close()
        return user
