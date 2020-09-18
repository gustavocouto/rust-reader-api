from mongoengine import *
from mongo.Compound import Compound
from mongo.User import User
from mongo.CompoundRead import CompoundRead
from mongo.MongoDoc import MongoDoc

class Label(MongoDoc):
    name = StringField(required=True)
    user = ReferenceField(User, required=True)
    compounds = EmbeddedDocumentListField(CompoundRead, default=[])

    def plain(self):
        doc = super().plain()
        doc['user'] = self.user.plain()
        return doc

    @staticmethod
    def page(skip, limit, restrict_user=None):
        query = Label.objects() if restrict_user is None else Label.objects(user=restrict_user)
        return query.skip(skip).limit(limit).all()

    @staticmethod
    def add(name, user, compounds):
        reads = []
        for compound in compounds:
            read = CompoundRead(name=compound['name'], accuracy=compound['accuracy'])
            if compound['best_match'] and compound['best_match']['_id']:
                read['best_match'] = Compound()
                read['best_match']['id'] = compound['best_match']['_id']
            reads.append(read)
        label = Label(name=name, user=user, compounds=reads)
        label.save()
        return label['id']
