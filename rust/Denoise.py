import numpy as np
from cv2 import cv2

class Denoise:
    def __init__(self, image):
        self.image = image

    def remove(self):
        return cv2.fastNlMeansDenoisingColored(self.image, None, 10, 10, 7, 15)