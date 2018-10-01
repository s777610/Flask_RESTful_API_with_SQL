import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# tell app where db could be found
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # is first not found, use sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True# return specific error that flask-jwt told you
app.secret_key = 'wilson'
api = Api(app)

# create db and all table before request, unless they exist already
@app.before_first_request
def create_tables():
    db.create_all()


"""
when user login, jwt will be generated
jwt is long access_token,
used for identify user
jwt create new endpoint /auth
"""

jwt = JWTManager(app)

"""
whenever we create a new access token(JWT),
we are going to run this func to see if we should add any extra data to JWT
"""
@jwt.user_claims_loader
def add_claims_to_jwt(identity): # identify is user.id in this case
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


"""if token expired"""
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# when the token users send us in authorization header is not jwt
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

# when user don't send us jwt at all
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(error):
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

api.add_resource(Store, '/store/<string:name>')
# http://127.0.0.1:5000/item/<name>
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
