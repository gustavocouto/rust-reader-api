from flask import *
from mongo.User import User

def read_token():
    return request.headers.get('token')

def get_user():
    return User.objects.get(id=get_user_id())

def get_user_id():
    return read_token()

def get_arg(arg, default=None):
    return request.args.get(arg) or default
    