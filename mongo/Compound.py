from mongoengine import *
from mongo.MongoDoc import MongoDoc
from functools import reduce

class Compound(MongoDoc):
    name = StringField(required=True)
    alergenic = BooleanField(default=False)
    sys_field = BooleanField(default=False)
    derived_names = ListField(StringField(), required=True)

    @staticmethod
    def search_by_names(names):
        return Compound.objects.filter(name__in=names)

    @staticmethod
    def track_or_save(compounds):
        names = [c['name'] for c in compounds]
        match = Compound.search_by_names(names)
        match_names = [m.name for m in match]
        umatch_reduct = lambda arr, _: arr if _['name'] in match_names else [*arr, Compound(name=_['name'])]
        umatch = reduce(umatch_reduct, compounds, [])
        umatch and Compound.objects.insert(umatch)
        return [*match, *umatch]

    @staticmethod
    def get_sys_compounds():
        return Compound.objects.filter(sys_field=True)