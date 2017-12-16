from models.user import UserModel

# users = [
#     User(1, 'bob', 'asdf')
# ]
# user_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    # .get gets the value of the key
    # user = user_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
