import json
from mongo.Ingredient import Ingredient

def sync():
    with open(__file__.replace('appenv/app_database.py', 'assets/ingredients.json')) as json_file:
        data = json.load(json_file)
        for ingredient_data in data:
            ingredient = Ingredient(name=ingredient_data['ingredient'])
            ingredient.save()
            for derived_name in ingredient_data['derivedNames']:
                derived_ingredient = Ingredient(name=derived_name, derived_from=ingredient)
                derived_ingredient.save()

def get_names():
    ingredients = list(Ingredient.objects())
    ingredients_names = [c['name'] for c in ingredients]
    with open(__file__.replace('appenv/app_database.py', 'assets/ingredients_names.txt')) as txt_file:
        for name in ingredients_names:
            txt_file.write(name + '\n')

def create_ingredients_file():
    ingredients = list(Ingredient.objects())
    with open(__file__.replace('appenv/app_database.py', 'assets/ingredients.psv'), 'w+') as txt_file:
        txt_file.write('id|name|derived_from_id|derived_from_name\n')
        for i in ingredients:
            line = f"{str(i['id'])}|{i['name']}|"
            derived_from = i['derived_from']
            if derived_from:
                line += f"{str(derived_from['id'])}|{derived_from['name']}\n"
            else:
                line += '|\n'
            txt_file.write(line)