import os
import numpy as np
import noise
import random
from PIL import Image
from Filter import Filter

SCRIPT_PATH = (os.path.dirname(os.path.abspath(__file__)))
SEED = random.randint(1,100000)

class Noisemap:
    def __init__(self, width, height, config):
        self.width = width
        self.height = height
        self.noise = config.noise
        self.filter = None
        self.filter_config = config.filters
        self.world = None # set in main
        self.load_filter(config.filters)
        self.__main(config.filters)

    def load_filter(self, filter_config):
        self.filter = Filter(filter_config['path'], filter_config['weight'])

    def __main(self, filter_config):
        # Make initial world filled with noise layers and pre-set filter
        # Values are constrained around 0 (typically between -0.3 and 0.3)
        self.make_noise()

        if self.filter is not None:
            self.subtract_filter(self.filter)

        # Change unbounded range to range of 0 and 1
        self.interpolate()

        # Creates an array from the interpolated world that adds land_bias 
        # and the second filter if necessary
        if self.filter_config['land_bias'] != 0.0: #and self.filter2 is not None:
            self.refine_world()

        self.add_color()
        self.image_output()

    def make_noise(self, filter_arr=None, filter_obj=None):
        #Create empty array
        self.world = np.zeros((self.height, self.width))

        #Fill world array with noise values and alter with filter
        for i in range(self.height):
            for j in range(self.width):
                #fill with noise
                self.world[i][j] = noise.pnoise3(i/self.noise['scale'], 
                                        j/self.noise['scale'], 
                                        SEED,
                                        octaves = self.noise['octaves'], 
                                        persistence = self.noise['persistence'], 
                                        lacunarity = self.noise['lacunarity'], 
                                        repeatx= self.width, 
                                        repeaty= self.height, 
                                        base= 0)

    def subtract_filter(self, filter_obj):
        self.world = np.subtract(self.world, 
                                    filter_obj.data * 
                                    filter_obj.weight)

    def interpolate(self):
        #Scales elements in an array to the range 0 and 1
        self.world = np.interp(self.world, 
                                (self.world.min(), self.world.max()), 
                                (0, 1))

    def refine_world(self):
        print("refined_world called")
        #Adds land bias and pre-set filter
        for i in range(self.height):
            for j in range(self.width):
                self.world[i][j] = self.world[i][j] + self.filter_config['land_bias'] #- ((filter2[i][j]) * filter2_bias)

    def add_color(self):
        #Zone Colors
        water_deep = [50,50,135]
        water_medium = [50,50,150]
        water_shallow = [50,50,165]
        sand_low = [195,180,125]
        sand_high = [165, 155, 95]
        fauna_low = [25,145,25]
        fauna_medium = [25,130,25]
        fauna_high = [25,115,25]
        
        #Color the world!
        colored_world = np.zeros(self.world.shape+(3,))

        colored_world[self.world < 0.28] = water_deep
        colored_world[(self.world >= 0.28) & (self.world < 0.38)] = water_medium 
        colored_world[(self.world >= 0.38) & (self.world < 0.46)] = water_shallow
        colored_world[(self.world >= 0.46) & (self.world < 0.48)] = sand_low
        colored_world[(self.world >= 0.48) & (self.world < 0.5)] = sand_high
        colored_world[(self.world >= 0.5) & (self.world < 0.6)] = fauna_low
        colored_world[(self.world >= 0.6) & (self.world < 0.7)] = fauna_medium
        colored_world[self.world >= 0.7] = fauna_high
        
        self.world = colored_world

    def get_stats(self):
        min_ = np.unravel_index(self.world.argmin(), self.world.shape)
        max_ = np.unravel_index(self.world.argmax(), self.world.shape)

        stats = {
            'min': {
                'value': self.world[min_[0]][min_[1]],
                'index': min_
            },
            'max': {
                'value': self.world[max_[0]][max_[1]],
                'index': max_
            }
        }
        return stats

    def image_output(self):
        ##converts array to a color image
        img = Image.fromarray((self.world).astype('uint8'), 'RGB')

        ##converts to black and white
        # img = Image.fromarray(np.uint8(self.world * 255) , 'L')

        # ##Image output options
        # ##shows image
        img.show()

        # ##saves as PNG file with name: "map{SEED}" to specified directory
        img.save(SCRIPT_PATH + f"\\maps\\map{SEED}.png")