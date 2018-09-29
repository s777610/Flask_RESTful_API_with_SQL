import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# tell app where db could be found
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # is first not found, use sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wilson'
api = Api(app)




"""
when user login, jwt will be generated
jwt is long access_token,
used for identify user
jwt create new endpoint /auth
"""
# after user login, every endpoint return JWT token
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
# http://127.0.0.1:5000/item/<name>
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
