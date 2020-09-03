import numpy as np
from PIL import Image

class Filter:
    def __init__(self, path, weight):
        self.path = path
        self.weight = weight
        self.data = None
        self.set_data()

    def set_data(self):
        ##load red value as grayscale ('g' or 'b' would work as well) 
        img = Image.open(self.path, mode="r").convert('L')
        ##save as array and divide by 255 to convert to range between 0 and 1
        self.data = np.array(img) / 255