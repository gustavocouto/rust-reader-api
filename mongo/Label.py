from mongoengine import *
from mongo.Compound import Compound
from mongo.User import User
from mongo.CompoundRead import CompoundRead
from mongo.MongoDoc import MongoDoc

class Label(MongoDoc):
    name = StringField(required=True)
    user = ReferenceField(User, required=True)
    compounds = ListField(ReferenceField(CompoundRead), default=[])

    def plain(self):
        doc = super().plain()
        doc['user'] = self.user.plain()
        return doc

    # @staticmethod
    # def find(id):

    @staticmethod
    def page(skip, limit, restrict_user=None):
        query = Label.objects() if restrict_user is None else Label.objects(user=restrict_user)
        return query.skip(skip).limit(limit).all()
