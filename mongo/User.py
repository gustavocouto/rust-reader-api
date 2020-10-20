from exceptions.ValidatorException import ValidatorException
from mongo.MongoDoc import MongoDoc
from mongo.Ingredient import Ingredient
from bson.objectid import ObjectId
from mongoengine import *

class User(MongoDoc):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    monster_name = StringField(required=False)
    priority_allergenics = ListField(ReferenceField(Ingredient), default=[])

    @staticmethod
    def email_exists(email, except_id=None):
        count = User.objects(email=email, id__ne=except_id).count()
        return count != 0

    def update_password(self, old_password, new_password):
        if old_password != self.password:
            raise ValidatorException(errors={'password': ['Senha atual incorreta']})
        super().update(set__password=new_password)

    def update(self, name=None, email=None, monster_name=None, priority_allergenics=None):
        name = name or self.name
        monster_name = monster_name or self.monster_name

        if email is not None:
            if User.email_exists(email, except_id=self['id']):
                raise ValidatorException(errors={'email': ['Esse e-mail ja está em uso']})
        else:
            email = self.email

        if priority_allergenics is not None:
            priority_allergenics = [ObjectId(a['id']) for a in priority_allergenics]
        else:
            priority_allergenics = self.priority_allergenics

        super().update(set__name=name, set__email=email, set__monster_name=monster_name, set__priority_allergenics=priority_allergenics)

    def save(self):
        user = User.objects.filter(Q(email=self.email))
        if user:
            raise ValidatorException(errors={'email': ['Esse email ja está em uso']})
        else:
            super().save()
            