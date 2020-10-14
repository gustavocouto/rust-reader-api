from mongoengine import *
from bson.objectid import ObjectId
from mongo.Ingredient import Ingredient
from mongo.User import User
from mongo.IngredientRead import IngredientRead
from mongo.MongoDoc import MongoDoc
from exceptions.ValidatorException import ValidatorException
import datetime

class Label(MongoDoc):
    name = StringField(required=True)
    user = ReferenceField(User, required=True)
    ingredients = EmbeddedDocumentListField(IngredientRead, default=[])
    created = DateTimeField(default=datetime.datetime.utcnow)

    @staticmethod
    def page(skip, limit, user, restrict_user, search=None):
        q_filter = Q(user=user) if restrict_user else Q(user__ne=user)
        q_filter = q_filter & Q(name__icontains=search.strip()) if search and search.strip() else q_filter
        return Label.objects(q_filter).order_by('-created').skip(skip).limit(limit).all()

    @staticmethod
    def add(name, user, ingredients):
        reads = []
        for ingredient in ingredients:
            read = IngredientRead(name=ingredient['name'], accuracy=ingredient['accuracy'])
            if ingredient['best_match'] and ingredient['best_match']['id'] and ingredient['best_match']['id'] != 'None':
                read['best_match'] = ObjectId(ingredient['best_match']['id'])
            reads.append(read)
        label = Label(name=name, user=user, ingredients=reads)
        label.save()
        return label['id']

    @staticmethod
    def remove(label, user):
        if label.user != user:
            raise ValidatorException(errors=[{'unauthorized': 'Você não tem permissão para excluir esse rótulo'}])
        label.delete()
