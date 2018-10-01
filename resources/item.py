
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
    )
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() # data is in body of request
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    # we have to authenticate(login) before calling this get method
    # need access token, identity() came into use
    @jwt_required # need fresh_token or non-fresh_token, wither of those will work
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    @fresh_jwt_required # need only fresh_token, means just login
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data) # **data = data['price'], data['store_id']
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error
        return item.json(), 201 # for created

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()



class ItemList(Resource):
    @jwt_optional
    def get(self):
        # this give us whatever we save in the access token as identity
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id: # check if users login
            return {'item': items}, 200
        return {'items': [item['name'] for item in items],
                'message': 'More data available if you log in.'}, 200
