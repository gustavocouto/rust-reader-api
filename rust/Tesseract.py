import operator
import pytesseract
import timeit
import difflib
from appenv import app_multiprocessing
from difflib import get_close_matches
from pytesseract import Output
from difflib import SequenceMatcher
from mongo.Ingredient import Ingredient
from mongo.IngredientRead import IngredientRead
from rust.PreProcess import *

class Tesseract:
    def __init__(self, image):
        self.image = image

    def pre_process(self):
        image = self.image
        image = resize_compress(image)
        image = grayscale(image)
        image = opening(image)
        image = thresholding(image, 170)
        image = invert_color(image)
        image = deskew(image)
        
        return image

    def get_text(self):
        image = self.pre_process()
        user_words_path = __file__.replace('rust/Tesseract.py', 'assets/user-words.txt')
        text = pytesseract.image_to_string(image, lang='por+eng', config='--user-words ' + user_words_path)
        return text.replace('\n', '')



        # load_freq_dawg
        # load_punc_dawg
        # load_number_dawg
        # load_unambig_dawg
        # load_bigram_dawg
        # load_fixed_length_dawgs')

    def get_matches(self):
        async def ingredients_p():
            return Ingredient.objects.values_list('name')
        async def image_text_p():
            image_text = self.get_text().replace(';', ',').replace(':', ',')
            return [text.strip() for text in image_text.split(',')]
        
        [ingredients, texts] = app_multiprocessing.process_all([ingredients_p(), image_text_p()])
        async def find_best_match(text):
            matches = difflib.get_close_matches(text, ingredients)
            best_match = matches[0] if matches else None
            accuracy = SequenceMatcher(None, best_match, text).ratio() if best_match else 0
            return IngredientRead(name=text, accuracy=accuracy, best_match=Ingredient(name=best_match))

        matches_tasks = [find_best_match(text) for text in texts]
        matches = app_multiprocessing.process_all(matches_tasks)
        matches_names = [match['best_match']['name'] for match in matches if match['best_match']['name']]
        matches_search = Ingredient.objects(name__in=matches_names)
        
        for match in matches:
            match_search = [search for search in matches_search if search['name'] == match['best_match']['name']]
            if match_search:
                match['best_match'] = match_search[0]
                
        return matches

    def get_matches_deadline(self, deadline):
        start = timeit.default_timer()
        matches = list(self.get_matches())
        end = timeit.default_timer()
        diff = end - start
        return [match for match in matches if match['accuracy'] > deadline]
