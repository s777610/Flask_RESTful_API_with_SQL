import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    jwt_optional
    )
from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )


################################################
## resource is external representation of entity
################################################
"""
Our API clients, such as a website or a mobile app,
think they're interacting with resources,
we can add it to API using flask restful
"""
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        user = UserModel(**data) # data is dict
        user.save_to_db()

        return {"message": "User created successfully." }, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    @jwt_optional
    def delete(cls, user_id):
        userid = get_jwt_identity()
        if userid == user_id:
            user = UserModel.find_by_id(user_id)
            user.delete_from_db()
            return {'message': 'User deleted.'}, 200
        else:
            return {'message': 'Authorization required'}, 401


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in db
        user = UserModel.find_by_username(data['username'])

        # check password
        if user and safe_str_cmp(user.password, data['password']):
            # flask_jwt_extended, it allow user to send token back to us to tell us who they are
            access_token = create_access_token(identity=user.id, fresh=True) # entering password so fresh is True
            refresh_token = create_refresh_token(user.id)
            # when user login, give user access/refresh token
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invlid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jti is a unique id for a jwt
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # here we have refresh token,
        # that means we can use it to get jwt_identity
        current_user = get_jwt_identity() # user.id in this case
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
