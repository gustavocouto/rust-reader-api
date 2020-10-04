from exceptions.ValidatorException import ValidatorException
from mongo.MongoDoc import MongoDoc
from mongo.Ingredient import Ingredient
from bson.objectid import ObjectId
from mongoengine import *

class User(MongoDoc):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    priority_allergenics = ListField(ReferenceField(Ingredient), default=[])

    def update(self, name=None, email=None, password=None, priority_allergenics=None):
        name = name or self.name
        email = email or self.email
        password = password or self.password
        if priority_allergenics is not None:
            priority_allergenics = [ObjectId(a['id']) for a in priority_allergenics]
        else:
            priority_allergenics = self.priority_allergenics

        super().update(set__name=name, set__email=email, set__password=password, set__priority_allergenics=priority_allergenics)

    def save(self):
        user = User.objects.filter(Q(email=self.email))
        if user:
            raise ValidatorException(errors={'user': ['Esse usuário ja está em uso']})
        else:
            super().save()
            