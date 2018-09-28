from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
# tell app where db could be found
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
# after user login, every endpoint return JWT token
jwt = JWT(app, authenticate, identity)


# http://127.0.0.1:5000/item/<name>
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
