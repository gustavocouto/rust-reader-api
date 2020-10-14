from mongoengine import *

class MongoDoc(Document):
    meta = {'abstract': True}

    def get(self, key, default=None):
        return self[key] if key in self else default