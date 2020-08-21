import numpy as np
from cv2 import cv2

class Deskew:
    def __init__(self, image):
        self.image = image

    def _find_threshold(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    def _find_angle(self, threshold):
        coords = np.column_stack(np.where(threshold > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        return angle

    def _rotate(self, angle):
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def correct(self):
        threshold = self._find_threshold()
        angle = self._find_angle(threshold)
        return self._rotate(angle)