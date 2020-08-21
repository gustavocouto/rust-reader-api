from rust.Deskew import Deskew
from rust.Binarization import Binarization
from rust.Denoise import Denoise

class Reader:
    def __init__(self, image):
        self.image = image

    def read(self):
        image = self.image
        image = Deskew(image).correct()
        image = Binarization(image).apply()
        image = Denoise(image).remove()

        return image