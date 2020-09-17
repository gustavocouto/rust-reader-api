import operator
import pytesseract
import timeit
import difflib
from appenv import app_multiprocessing
from rapidfuzz import process
from difflib import get_close_matches
from pytesseract import Output
from difflib import SequenceMatcher
from mongo.Compound import Compound
from rust.PreProcess import *

class Tesseract:
    def __init__(self, image):
        self.image = image

    def pre_process(self):
        image = self.image
        image = resize_compress(image)
        image = grayscale(image)
        # image = remove_noise(image)
        # grays = find_grays(image)
        # dilated = canny(image)
        # thresh_fact = find_thresholding_fact(image)
        image = thresholding(image, 160)
        image = invert_color(image)
        
        
        # image = canny(image)
        # image = erode(image)
        # image = dilate(image)
        
        # image = invert_color_when_black(image)
        
        image = deskew(image)
        # image = canny(image)
        
        return image

    def get_text(self):
        image = self.pre_process()
        config = '-c load_freq_dawg=F load_punc_dawg=F load_number_dawg=F load_unambig_dawg=F load_bigram_dawg=F load_fixed_length_dawgs=F language_model_penalty_non_freq_dict_word=1 language_model_penalty_non_dict_word=1'
        user_words_path = __file__.replace('Tesseract.py', 'user-words')
        text = pytesseract.image_to_string(image, lang='por+eng', config='--user-words ' + user_words_path)
        return text.replace('\n', '')
        # load_freq_dawg
        # load_punc_dawg
        # load_number_dawg
        # load_unambig_dawg
        # load_bigram_dawg
        # load_fixed_length_dawgs')

    def get_matches(self):
        async def compounds_p():
            return Compound.objects.values_list('name')
        async def image_text_p():
            image_text = self.get_text().replace(';', ',').replace(':', ',')
            return [text.strip() for text in image_text.split(',')]
        
        [compounds, texts] = app_multiprocessing.process_all([compounds_p(), image_text_p()])
        async def find_best_match(text):
            # best_match = process.extractOne(text, compounds)
            matches = difflib.get_close_matches(text, compounds)
            best_match = matches[0] if matches else None
            accuracy = SequenceMatcher(None, best_match, text).ratio() if best_match else 0
            # ratios = [{'accuracy': SequenceMatcher(None, compound['name'], text).ratio(), 'best_match': compound.plain()} for compound in compounds]
            # ratio_max = max(ratios, key=lambda ratio: ratio['accuracy'])
            return {'name': text, 'best_match': {'name': best_match}, 'accuracy': accuracy}

        tasks = [find_best_match(text) for text in texts]
        return app_multiprocessing.process_all(tasks)

    def get_matches_deadline(self, deadline):
        start = timeit.default_timer()
        matches = list(self.get_matches())
        end = timeit.default_timer()
        diff = end - start
        return [match for match in matches if match['accuracy'] > deadline]
