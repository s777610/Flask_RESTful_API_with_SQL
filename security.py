from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username) # return None if not found
    if user and safe_str_cmp(user.password, password):
        return user


"""
The word payload, in most programming scenarios,
refers to the data transferred with a certain action.
For example, when users try to login, users need to provide data(username, password),
the payload is the username and password. So in the identity()
we can assume that the payload must contain some info about the JWT and the current user,
among which is the user's identity (user id).
"""
# identity is used to retrieve currently logged-in user's identity
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
