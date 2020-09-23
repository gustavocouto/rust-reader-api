from mongoengine import *
from mongo.Compound import Compound
from flask import jsonify
from bson.objectid import ObjectId

def to_json(obj):
    plained = plain(obj)
    return jsonify(plained)

# def plain(obj):
#     if obj is None:
#         return obj
#     if isinstance(obj, list):
#         return [plain(i) for i in obj]

#     fields = {}
#     for obj_field in obj:
#         field = obj[obj_field]
#         if isinstance(field, ObjectId):
#             fields[obj_field] = str(field)
#         elif isinstance(field, list):
#             fields[obj_field] = [plain(i) for i in field]
#         elif isinstance(field, dict) or isinstance(field, Document):
#             fields[obj_field] = plain(field)
#         else:
#             fields[obj_field] = field
#     return fields

def plain(obj):
    def object_or_id(target, parse, parse_name):
        oid = None
        if isinstance(target, ObjectId):
            oid = str(target)
        elif isinstance(target, parse):
            oid = exec_parse(parse_name, target)
        return oid

    def exec_parse(name, target):
        return None if target is None else parses[name](target)

    def compound(target):
        return {
            'id': str(target['id']),
            'name': target['name'],
            'derived_from': exec_parse('Compound', target['derived_from'])
        }

    def compound_read(target):
        return {
            'name': target['name'],
            'accuracy': target['accuracy'],
            'best_match': object_or_id(target['best_match'], Compound, 'Compound')
        }
    
    def label(target):
        return {
            'id': str(target['id']),
            'name': target['name'],
            'user': exec_parse('User', target['user']),
            'compounds': [exec_parse('CompoundRead', c) for c in target['compounds']],
            'created': target['created']
        }

    def user(target):
        return {
            'id': str(target['id']),
            'name': target['name'],
            'email': target['email'],
            'priority_allergenics': [object_or_id(p, Compound, 'Compound') for p in target['priority_allergenics']]
        }

    parses = {
        'Compound': compound,
        'CompoundRead': compound_read,
        'Label': label,
        'User': user
    }

    if isinstance(obj, list):
        if len(obj) == 0:
            return []
        name = type(obj[0]).__name__
        return [exec_parse(name, o) for o in obj]
    else:
        name = type(obj).__name__
        return exec_parse(name, obj)