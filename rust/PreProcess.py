import numpy as np
from functools import *
from statistics import median
from collections import Counter
from multiprocessing import Process, Manager
from cv2 import cv2 

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.GaussianBlur(image, (5, 5), 1)

#thresholding
def thresholding(image, fact):
    # thre = cv2.threshold(image, fact, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)[1]
    
    thre = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)[1]
    
    # thre = cv2.threshold(thre, 127, 255, cv2.THRESH_OTSU)[1]
    return thre

#dilation
def dilate(image):
    kernel = np.ones((1,2), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

#erosion
def erode(image):
    kernel = np.ones((1,2))
    return cv2.erode(image, kernel, iterations=4)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((1, 2), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

def invert_color(image):
    whites = cv2.countNonZero(image)
    blacks = image.size - whites
    if blacks > whites:
        return cv2.bitwise_not(image)
    else:
        return image

def resize_compress(image):
    height, width = image.shape[:2]
    max_height = 1000
    max_width = 1000

    if max_height < height or max_width < width:
        scaling_factor = max_height / float(height)
        if max_width/float(width) < scaling_factor:
            scaling_factor = max_width / float(width)
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return image

def find_thresholding_fact(image):
    thre = thresholding(image, 127)
    rows = range(thre.shape[0])
    columns = range(thre.shape[1])
    pixels = [{'black': thre[x][y] == 0, 'coord': (x, y)} for x in rows for y in columns]
    blacks = len([pixel for pixel in pixels if pixel['black']])
    whites = len([pixel for pixel in pixels if not pixel['black']])
    restrict_blacks = blacks < whites
    fore_pixels = [pixel['coord'] for pixel in pixels if pixel['black'] == restrict_blacks]
    fore_grays = [image[pixel[0]][pixel[1]] for pixel in fore_pixels]
    counts = sorted(Counter(fore_grays).items(), key=lambda x: x[1], reverse=True)
    # counts_middle = [count[0] for count in counts[:10]] + [count[0] for count in counts[-5:]]
    return int(np.median(np.array(counts)))

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)