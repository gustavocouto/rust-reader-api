from mongoengine import *
from mongo.Compound import Compound
from mongo.User import User
from mongo.MongoDoc import MongoDoc

class Label(MongoDoc):
    name = StringField(required=True)
    user = ReferenceField(User, required=True)
    private = BooleanField(required=True, default=False)
    compounds = ListField(ReferenceField(Compound), default=[])


    def plain(self):
        doc_mongo = super().plain()
        doc_mongo['user'] = self.user.plain()
        return doc_mongo

    # @staticmethod
    # def find(id):


    @staticmethod
    def page(self, skip, limit, restrict_user=None):
        query = Label.objects(user=restrict_user) if restrict_user else Label.objects()
        return query.skip(skip).limit(limit).all()