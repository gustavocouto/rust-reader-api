from mongoengine import *

class MongoDoc(Document):
    meta = {'abstract': True}

    def plain(self):
        doc = self.to_mongo()
        doc['_id'] = str(doc['_id'])
        return doc