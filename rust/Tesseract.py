import pytesseract
from pytesseract import Output
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
        image = thresholding(image, 127)
        # image = erode(image)
        
        
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
        return pytesseract.image_to_string(image, lang='por+eng', config='--user-words ' + user_words_path)
        # load_freq_dawg
        # load_punc_dawg
        # load_number_dawg
        # load_unambig_dawg
        # load_bigram_dawg
        # load_fixed_length_dawgs')

    def get_matches(self):
        compounds = Compound.get_sys_compounds()
        image_text = self.get_text().lower()
        compounds_m = [compound for compound in compounds if compound['name'] in image_text]
        return compounds_m
