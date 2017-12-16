from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(slef, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        # Below returns a tuple
        return {'Message': 'Store is not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return "A store with name '{}' already exists...".format(name), 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'Message': 'An error occured creating the store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'Message': 'Store is deleted'}

class StoreList(Resource):
    def get(self):
        return {
            'Stores': [store.json() for store in StoreModel.query.all()]
        }
