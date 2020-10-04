import json
from mongo.Ingredient import Ingredient

def sync():
    with open(__file__.replace('app_database.py', 'ingredients.json')) as json_file:
        data = json.load(json_file)
        for ingredient_data in data:
            ingredient = Ingredient(name=ingredient_data['ingredient'])
            ingredient.save()
            for derived_name in ingredient_data['derivedNames']:
                derived_ingredient = Ingredient(name=derived_name, derived_from=ingredient)
                derived_ingredient.save()
            