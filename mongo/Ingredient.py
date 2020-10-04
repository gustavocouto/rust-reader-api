from mongoengine import *
from mongo.MongoDoc import MongoDoc
from functools import reduce

class Ingredient(MongoDoc):
    name = StringField(required=True)
    derived_from = ReferenceField('self', required=False)

    # def plain(self):
    #     doc = super().plain()
    #     doc['derived_from'] = str(self.derived_from)
    #     return doc

    @staticmethod
    def search_by_names(names):
        return Ingredient.objects.filter(name__in=names)

    @staticmethod
    def page(skip, limit, search=None):
        pipelines = [
            {
                '$project': {
                    'reference': {
                        '$ifNull': ['$derived_from', '$_id']
                    },
                    'target': '$$ROOT'
                }
            },
            {
                '$group': {
                    '_id': '$reference',
                    'ingredients': {'$push': '$target'}
                }
            },
            {
                '$match': {
                    'ingredients': {
                        '$elemMatch': {'name': {'$regex': '.*' + (search or '') + '.*'}}
                    }
                }
            },
            {
                '$project': {
                    'ingredient': {
                        '$filter': {
                            'input': '$ingredients',
                            'as': 'item',
                            'cond': {
                                '$eq': ['$derived_from', '$id']
                            }
                        }
                    },
                    'derived_ingredients': {
                        '$filter': {
                            'input': '$ingredients',
                            'as': 'item',
                            'cond': {
                                '$ifNull': ['$$item.derived_from', False]
                            }
                        }
                    }
                }
            },
            {
                '$project': {
                    'ingredient': {
                        '$arrayElemAt': ['$ingredient', 0]
                    },
                    'derived_ingredients': {
                        '$map': {
                            'input': '$derived_ingredients',
                            'as': 'item',
                            'in': {
                                '_id': '$$item._id',
                                'name': '$$item.name'
                            }
                        }
                    }
                }
            },
            {
                '$sort': {
                    'ingredient.name': 1
                }
            },
            {
                '$unset': '_id'
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
            }
        ]

        return Ingredient.objects().aggregate(pipelines)

    # @staticmethod
    # def track_or_save(ingredients):
    #     names = [c['name'] for c in ingredients]
    #     match = Ingredient.search_by_names(names)
    #     match_names = [m.name for m in match]
    #     umatch_reduct = lambda arr, _: arr if _['name'] in match_names else [*arr, Ingredient(name=_['name'])]
    #     umatch = reduce(umatch_reduct, ingredients, [])
    #     umatch and Ingredient.objects.insert(umatch)
    #     return [*match, *umatch]