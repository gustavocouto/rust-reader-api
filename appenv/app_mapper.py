from mongoengine import *
from mongo.Ingredient import Ingredient
from flask import jsonify
from bson.objectid import ObjectId

def to_json(obj, target_type=None):
    plained = plain(obj, target_type)
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

def plain(obj, target_type=None):
    def object_or_id(target, parse, parse_name):
        oid = None
        if isinstance(target, ObjectId):
            oid = str(target)
        elif isinstance(target, parse):
            oid = exec_parse(parse_name, target)
        return oid

    def exec_parse(name, target):
        return None if target is None else parses[name](target)

    def ingredient(target):
        return {
            'id': str(target.get('_id') or target.get('id')),
            'name': target.get('name'),
            'derived_from': exec_parse('Ingredient', target.get('derived_from'))
        }

    def ingredient_read(target):
        return {
            'name': target.get('name'),
            'accuracy': target.get('accuracy'),
            'best_match': object_or_id(target.get('best_match'), Ingredient, 'Ingredient')
        }
    
    def label(target):
        return {
            'id': str(target.get('id')),
            'name': target.get('name'),
            'user': exec_parse('User', target.get('user')),
            'ingredients': [exec_parse('IngredientRead', c) for c in target.get('ingredients', [])],
            'created': target.get('created')
        }

    def user(target):
        return {
            'id': str(target['id']),
            'name': target.get('name'),
            'email': target.get('email'),
            'priority_allergenics': [object_or_id(p, Ingredient, 'Ingredient') for p in target.get('priority_allergenics', [])],
            'private_account': target.get('private_account')
        }

    def derived_ingredients(target):
        return {
            'ingredient': exec_parse('Ingredient', target.get('ingredient')),
            'derived_ingredients': [exec_parse('Ingredient', i) for i in target.get('derived_ingredients', )]
        }

    parses = {
        'Ingredient': ingredient,
        'IngredientRead': ingredient_read,
        'Label': label,
        'User': user,
        'DerivedIngredients': derived_ingredients
    }

    if isinstance(obj, list):
        if len(obj) == 0:
            return []
        name = target_type or type(obj[0]).__name__
        return [exec_parse(name, o) for o in obj]
    else:
        name = target_type or type(obj).__name__
        return exec_parse(name, obj)