import flask
import os
from bson.objectid import ObjectId
from cerberus import Validator
from flask import request, jsonify
from flask_cors import CORS
from mongo.User import User
from mongo.Label import Label
from mongo.Ingredient import Ingredient
from mongoengine import connect
from json import dumps
from inspect import isclass
from appenv import app_context, app_validations, app_database, app_mapper
from exceptions.ValidatorException import ValidatorException

from cv2 import cv2
from rust.Tesseract import Tesseract

app = flask.Flask(__name__)
CORS(app)
connect(host='mongodb+srv://admin:admin@schoolcluster.s8zzy.gcp.mongodb.net/rustreader?retryWrites=true&w=majority')

def read_json_request(validator_schema=None):
    json = request.get_json()
    if validator_schema:
        validator = Validator(validator_schema, ignore_none_values=True)
        if not validator.validate(json):
            raise ValidatorException(validator)
    return json

@app.errorhandler(ValidatorException)
def handle_invalid_usage(error):
    response = jsonify(error.errors)
    response.status_code = error.status_code
    return response

@app.route('/api/test', methods=['GET']):
    if request.method == 'GET':
        return jsonify('API is ready')

@app.route('/api/auth', methods=['POST'])
def auth():
    if request.method == 'POST':
        json = read_json_request()
        user = User.objects.get(email=json['email'], password=json['password'])
        if not user:
            raise ValidatorException(errors=[{'user': 'Usuário não encontrado ou senha incorreta'}])
        json = app_mapper.plain(user)
        return jsonify({ 'token': str(user.pk), 'user': json })

@app.route('/api/users', methods=['POST', 'PUT'])
def user():
    if request.method == 'POST':
        json = read_json_request(app_validations.user_create_schema)
        user = User(name=json['name'], email=json['email'], password=json['password'])
        user.save()
        return app_mapper.to_json(user)
    if request.method == 'PUT':
        json = read_json_request(app_validations.user_create_schema)
        user = app_context.get_user()
        user.update(name=json['name'], email=json['email'], priority_allergenics=json['priority_allergenics'])
        return str(user['id'])

@app.route('/api/labels', methods=['GET', 'POST'])
def get_labels():
    if request.method == 'GET':
        user = app_context.get_user()
        search = app_context.get_arg('search')
        restrict_user = app_context.get_arg('strict') == 'me'
        labels = Label.page(app_context.get_arg('skip', 0), app_context.get_arg('limit', 20), user, restrict_user, search)
        return app_mapper.to_json(list(labels))
    if request.method == 'POST':
        json = read_json_request(app_validations.label_create_schema)
        user = app_context.get_user()
        label_id = Label.add(name=json['name'], user=user, ingredients=json['ingredients'])
        return jsonify(str(label_id))

@app.route('/api/labels/<label_id>', methods=['GET', 'DELETE'])
def get_label(label_id):
    if request.method == 'GET':
        label = Label.objects.get(id=ObjectId(label_id))
        return app_mapper.to_json(label)
    if request.method == 'DELETE':
        label = Label.objects.get(id=ObjectId(label_id))
        user = app_context.get_user()
        Label.remove(label, user)
        return jsonify(True)

@app.route('/api/read', methods=['POST'])
def read():
    if request.method == 'POST':
        image = app_context.read_image()
        tesseract = Tesseract(image)
        matches = tesseract.get_matches()
        return app_mapper.to_json(list(matches))

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    if request.method == 'GET':
        search = app_context.get_arg('search')
        skip = int(app_context.get_arg('skip', 0))
        limit = int(app_context.get_arg('limit', 20))
        ingredients = Ingredient.page(skip, limit, search)
        return app_mapper.to_json(list(ingredients), 'DerivedIngredients')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# file_path = __file__.replace('app.py', 'rotulo.jpg')
# image = cv2.imread(file_path)
# tesseract = Tesseract(image)
# # okok = tesseract.get_text()
# pre = tesseract.pre_process()
# text = tesseract.get_text().replace('\n', '')
# cv2.imshow('img', pre)
# cv2.waitKey(0)