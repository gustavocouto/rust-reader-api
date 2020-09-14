from flask import *
import numpy as np
from cv2 import cv2
from mongo.User import User

def read_token():
    token = request.environ['HTTP_AUTHORIZATION']
    token = token if token is None else token.replace('Bearer ', '')
    return token

def get_user():
    return User.objects.get(id=get_user_id())

def get_user_id():
    return read_token()

def get_arg(arg, default=None):
    return request.args.get(arg) or default

def read_image():
    filestr = request.files.get('image')
    npimg = np.fromfile(filestr, np.uint8)
    return cv2.imdecode(npimg, cv2.IMREAD_COLOR)
