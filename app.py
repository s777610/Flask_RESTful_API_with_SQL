from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
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


# http://127.0.0.1:5000/item/<name>
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
