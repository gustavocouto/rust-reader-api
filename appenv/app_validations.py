"""Response JSON validator schemes"""

ingredient_schema = {
    'id': {'type': 'string'},
    'name': {'type': 'string'},
    'derived_from': {'type': 'dict', 'schema': {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'derived_from': {'type': 'string', 'required': False}
    }, 'required': False}
}

user_create_schema = {
    'id': {'required': False, 'type': 'string'},
    'monster_name': {'required': False, 'type': 'string', 'minlength': 3, 'maxlength': 100},
    'name': {'required': True, 'type': 'string', 'minlength': 3, 'maxlength': 100},
    'password': {'required': False, 'type': 'string', 'minlength': 3, 'maxlength': 150},
    'email': {'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 100},
    'priority_allergenics': {'required': False, 'type': 'list', 'schema': {
            'type': 'dict',
            'schema': ingredient_schema
        }
    }
}

label_create_schema = {
    'name': {'type': 'string'},
    'ingredients': {'type': 'list', 'schema': {
            'type': 'dict',
            'schema': {
                'id': {'type': 'string'},
                'accuracy': {'type': 'number'},
                'name': {'type': 'string'},
                'best_match': {'type': 'dict', 'schema': ingredient_schema, 'required': False}
            }
        }
    }
}
