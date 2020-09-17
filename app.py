import flask
import os
from cerberus import Validator
from flask import request, jsonify
from flask_cors import CORS
from mongo.User import User
from mongo.Label import Label
from mongo.Compound import Compound
from mongoengine import connect
from json import dumps
from inspect import isclass
from appenv import app_context, app_validations, app_database
from exceptions.ValidatorException import ValidatorException

from cv2 import cv2
from rust.Tesseract import Tesseract

app = flask.Flask(__name__)
CORS(app)
connect(host='mongodb+srv://admin:admin@schoolcluster.s8zzy.gcp.mongodb.net/rustreader?retryWrites=true&w=majority')

def read_json_request(validator_schema=None):
    json = request.get_json()
    if validator_schema:
        validator = Validator(validator_schema)
        if not validator.validate(json):
            raise ValidatorException(validator)
    return json

@app.errorhandler(ValidatorException)
def handle_invalid_usage(error):
    response = jsonify(error.errors)
    response.status_code = error.status_code
    return response

@app.route('/api/test', methods=['GET'])
def test():
    if request.method == 'GET':
        return jsonify('Api is working')

@app.route('/api/auth', methods=['POST'])
def auth():
    if request.method == 'POST':
        json = read_json_request()
        user = User.objects.filter(email=json['email'], password=json['password'])
        if not user:
            raise ValidatorException(errors=[{'user': 'Usuário não encontrado ou senha incorreta'}])
        response = flask.Response(dumps(user.plain()), headers={'token': str(user.pk)}, mimetype="application/json")
        return response

@app.route('/api/user', methods=['POST', 'PUT'])
def user():
    if request.method == 'POST':
        json = read_json_request(app_validations.user_create_schema)
        user = User(name=json['name'], email=json['email'], password=json['password'])
        user.save()
        return jsonify(user.plain())
    if request.method == 'PUT':
        json = read_json_request(app_validations.user_create_schema)
        user = app_context.get_user()
        user.update(name=json['name'], priority_allergenics=json['priority_allergenics'], private_account=json['settings']['private_account'])
        return str(user['id'])

@app.route('/api/label', methods=['GET'])
def get_labels():
    if request.method == 'GET':
        me = app_context.get_arg('me')
        user = app_context.get_user()
        labels = Label.page(app_context.get_arg('skip', 0), app_context.get_arg('limit', 20), user)
        labels_plain = [label.plain() for label in list(labels)]
        return jsonify(labels_plain)

@app.route('/api/label/<label_id>', methods=['GET'])
def get_label(label_id):
    if request.method == 'GET':
        label = Label.objects.get(id=label_id)
        return jsonify(label.plain())

@app.route('/api/read', methods=['POST'])
def read():
    if request.method == 'POST':
        image = app_context.read_image()
        tesseract = Tesseract(image)
        matches = tesseract.get_matches_deadline(float(0))
        return jsonify([match for match in matches])

@app.route('/api/label', methods=['POST'])
def add_label():
    if request.method == 'POST':
        json = read_json_request(app_validations.label_create_schema)
        user = app_context.get_user()
        compounds = Compound.track_or_save(json['compounds'] or [])
        label = Label(name=json['name'], user=user, compounds=compounds)
        label.save()
        return jsonify(label.plain())

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