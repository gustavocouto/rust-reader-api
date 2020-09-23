from exceptions.ValidatorException import ValidatorException
from mongo.MongoDoc import MongoDoc
from mongo.Compound import Compound
from mongoengine import *

class User(MongoDoc):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    priority_allergenics = ListField(ReferenceField(Compound), default=[])
    settings = DictField()

    # def plain(self):
    #     doc_mongo = super().plain()
    #     del doc_mongo['password']
    #     return doc_mongo

    def update(self, name=None, email=None, password=None, priority_allergenics=[], private_account=None):
        name = name or self.name
        email = email or self.email
        password = password or self.password
        private_account = self.settings['private_account'] if private_account is None else private_account
        super().update(set__name=name, set__email=email, set__password=password, set__settings__priority_allergenics=priority_allergenics, set__settings__private_account=private_account)

    def save(self):
        user = User.objects.filter(Q(email=self.email))
        if user:
            raise ValidatorException(errors={'user': ['Esse usuário ja está em uso']})
        else:
            super().save()
            