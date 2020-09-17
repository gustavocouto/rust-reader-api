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

label_create_schema = {
    'name': {'required': True, 'type': 'string', 'minlength': 3, 'maxlength': 100},
    'compounds': {'required': False, 'type': 'list', 'schema': {
            'type': 'dict',
            'schema': {
                'name': {'type': 'string', 'minlength': 3, 'maxlength': 100}
            }
        }
    }
}
