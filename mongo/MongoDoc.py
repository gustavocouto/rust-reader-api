from mongoengine import *

class MongoDoc(Document):
    meta = {'abstract': True}

    def plain(self):
        doc_mongo = self.to_mongo()
        doc_mongo['_id'] = str(doc_mongo['_id'])
        return doc_mongo