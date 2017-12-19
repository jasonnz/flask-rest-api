import sys

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

print('Python version = ', sys.version)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Store,  '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# main is the file that is run when running form the command line
# But it is different through uwsgi
# This is here because of circular imports
if __name__ == '__main__':
# if __name__ == 'app':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
