from mongoengine import *
from mongo.MongoDoc import MongoDoc
from mongo.Compound import Compound

class CompoundRead(MongoDoc):
    name = StringField(required=True)
    accuracy = FloatField(required=True, default=0)
    best_match = ReferenceField(Compound, required=False)