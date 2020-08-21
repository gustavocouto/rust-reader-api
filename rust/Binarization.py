from cv2 import cv2

class Binarization:
    def __init__(self, image):
        self.image = image

    def apply(self):
        ret, image = cv2.threshold(self.image, 128, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)
        return image