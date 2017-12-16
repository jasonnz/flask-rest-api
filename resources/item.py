# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
# import os.path

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # db_path = os.path.join('../', BASE_DIR, "data.db")
db_path = './data.db'

class Item(Resource):

    parser = reqparse.RequestParser()
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

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # Puts the filter returned object into a list
        # item = list(filter(lambda x: x['name'] == name, items))
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        
        return {'error': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return "An item with name '{}' already exists...".format(name), 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        # items.append(item)

        try:
            item.save_to_db()
        except Exception as error:
            return {"message": "An error has occured, {} ,inserting the item !{}!".format(error, 'ERROR')}, 500
        finally:
            pass
        
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
           item.delete_from_db()
        
        return {"message": "The item has been deleted"}, 204


    def put(self, name):
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store = data['store_id']

        item.save_to_db()
        
        return item.json()

        
class ItemList(Resource):
    def get(self):
        array = [item.json() for item in ItemModel.query.all()]
        print('Items ', array)   # 'Items': list(map(lamda x: x.json, ItemModel.query.all()))
        return { 
            'Items': array 
        }
