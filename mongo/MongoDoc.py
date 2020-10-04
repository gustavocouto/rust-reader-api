from mongoengine import *

class MongoDoc(Document):
    meta = {'abstract': True}

    def get(self, key, default=None):
        return self[key] if key in self else default

    # def plain(self):
    #     doc = self.to_mongo()
    #     doc['_id'] = str(doc['_id'])
    #     return doc