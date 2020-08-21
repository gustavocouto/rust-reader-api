from exceptions.ValidatorException import ValidatorException
from mongo.MongoDoc import MongoDoc
from mongoengine import *

class User(MongoDoc):
    name = StringField(required=True)
    email = StringField(required=True)
    picture = ImageField()
    password = StringField(required=True)

    def plain(self):
        doc_mongo = super().plain()
        del doc_mongo['password']
        return doc_mongo

    def save(self):
        user = User.objects.filter(Q(email=self.email))
        if user:
            raise ValidatorException(errors={'user': ['Esse usuário ja está em uso']})
        else:
            super().save()
            