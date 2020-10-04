from mongoengine import *
from mongo.MongoDoc import MongoDoc
from mongo.Ingredient import Ingredient

class IngredientRead(EmbeddedDocument):
    name = StringField(required=True)
    accuracy = FloatField(required=True, default=0)
    best_match = ReferenceField(Ingredient, required=False)

    def get(self, key, default=None):
        return self[key] if key in self else default
