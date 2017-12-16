import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

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
        
        if not data:
            return {'error': 'No username or password supplied'}, 401 

        if UserModel.find_by_username(data['username']) is not None:
            return {'error': 'A user with that username does already exist'}
        
        # **variable unpacks the key values inthe dictionary
        user = UserModel(**data)
        # print('user = UserModel(**data) ', data['username'], data['password'])
        user.save_to_db()

        return {'message': 'The user was created succesfully.'}, 201

    def get(self):
        return {
            'Users': [user.json() for user in UserModel.query.all()]
        }
