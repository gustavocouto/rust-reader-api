import json
from mongo.Compound import Compound

def sync():
    with open(__file__.replace('app_database.py', 'compounds.json')) as json_file:
        data = json.load(json_file)
        for compound_data in data:
            compound = Compound(name=compound_data['compound'])
            compound.save()
            for derived_name in compound_data['derivedNames']:
                derived_compound = Compound(name=derived_name, derived_from=compound)
                derived_compound.save()
            