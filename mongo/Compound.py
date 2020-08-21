from mongoengine import *
from mongo.MongoDoc import MongoDoc
from functools import reduce

class Compound(MongoDoc):
    name = StringField(required=True)
    alergenic = BooleanField(default=False)
    sys_field = BooleanField(default=False)
    derived_from = ReferenceField('self')

    @staticmethod
    def search_by_names(names):
        return Compound.objects.filter(name__in=names)

    @staticmethod
    def track_or_save(compounds):
        names = [_['name'] for _ in compounds]
        match = Compound.search_by_names(names)
        match_names = [_.name for _ in match]
        umatch_reduct = lambda arr, _: arr if _['name'] in match_names else [*arr, Compound(name=_['name'])]
        umatch = reduce(umatch_reduct, compounds, [])
        umatch and Compound.objects.insert(umatch)
        return [*match, *umatch]
