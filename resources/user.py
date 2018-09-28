import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

################################################
## resource is external representation of entity
################################################
"""
Our API clients, such as a website or a mobile app,
think they're interacting with resources,
we can add it to API using flask restful
"""
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )


    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data) # data is dict
        user.save_to_db()

        return {"message": "User created successfully." }, 201
