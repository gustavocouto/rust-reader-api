"""Response JSON validator schemes"""

user_create_schema = {
    'name': {'required': True, 'type': 'string', 'minlength': 3, 'maxlength': 100},
    'password': {'required': True, 'type': 'string', 'minlength': 3, 'maxlength': 150},
    'email': {'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 100},
    'settings': {'required': False, 'type': 'dict', 'schema': {
            'private_account': {'type': 'boolean', 'required': False}
        }
    }
}

compound_schema = {
    '_id': {'type': 'string'},
    'name': {'type': 'string'},
    'derived_from': {'type': 'string'}
}

label_create_schema = {
    'name': {'type': 'string'},
    'compounds': {'type': 'list', 'schema': {
            'type': 'dict',
            'schema': {
                '_id': {'type': 'string'},
                'accuracy': {'type': 'number'},
                'name': {'type': 'string'},
                'best_match': {'type': 'dict', 'schema': compound_schema}
            }
        }
    }
}
