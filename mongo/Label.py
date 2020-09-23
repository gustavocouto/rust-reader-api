from mongoengine import *
from bson.objectid import ObjectId
from mongo.Compound import Compound
from mongo.User import User
from mongo.CompoundRead import CompoundRead
from mongo.MongoDoc import MongoDoc
from exceptions.ValidatorException import ValidatorException
import datetime

class Label(MongoDoc):
    name = StringField(required=True)
    user = ReferenceField(User, required=True)
    compounds = EmbeddedDocumentListField(CompoundRead, default=[])
    created = DateTimeField(default=datetime.datetime.utcnow)

    # def plain(self):
    #     doc = super().plain()
    #     doc['user'] = self.user.plain()
    #     doc['created'] = self.created.isoformat()
    #     doc['compounds'] = [c.plain() for c in self.compounds]
    #     return doc

    @staticmethod
    def page(skip, limit, user, restrict_user, search=None):
        q_filter = Q(user=user) if restrict_user else Q(user__ne=user)
        q_filter = q_filter & Q(name__icontains=search.strip()) if search and search.strip() else q_filter
        return Label.objects(q_filter).order_by('-created').skip(skip).limit(limit).all()

    @staticmethod
    def add(name, user, compounds):
        reads = []
        for compound in compounds:
            read = CompoundRead(name=compound['name'], accuracy=compound['accuracy'])
            if compound['best_match'] and compound['best_match']['id'] and compound['best_match']['id'] != 'None':
                read['best_match'] = ObjectId(compound['best_match']['id'])
            reads.append(read)
        label = Label(name=name, user=user, compounds=reads)
        label.save()
        return label['id']

    @staticmethod
    def remove(label, user):
        if label.user != user:
            raise ValidatorException(errors=[{'unauthorized': 'Você não tem permissão para excluir esse rótulo'}])
        label.delete()
