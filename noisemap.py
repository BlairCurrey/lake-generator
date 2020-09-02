import os
import numpy as np
import noise
from PIL import Image
from filter_ import filter_

SCRIPT_PATH = (os.path.dirname(os.path.abspath(__file__)))

class noisemap:
    def __init__(self, settings):
        self.settings = settings
        self.filter_ = None
        self.load_filter(settings.filters)
        self.world = None
        self.colored_world = None

        self.__main(settings.filters)

    def load_filter(self, filter_settings):
        self.filter_ = filter_(filter_settings['path'], filter_settings['weight'])

    def __main(self, filter_settings):
        # Make initial world filled with noise layers and pre-set filter
        # Values are constrained around 0 (typically between -0.3 and 0.3)
        self.make_noise()

        if self.filter_ is not None:
            self.subtract_filter(self.filter_)

        # Change unbounded range to range of 0 and 1
        self.interpolate()

        # Creates an array from the interpolated world that adds land_bias 
        # and the second filter if necessary
        if self.settings.filters['land_bias'] != 0.0: #and self.filter_2 is not None:
            self.refine_world()

        self.add_color()
        self.save_img()

    def make_noise(self, filter_arr=None, filter_obj=None):
        #Create empty array
        height = self.settings.img['y']
        width = self.settings.img['x']
        self.world = np.zeros((height, width))

        #save relevant settings
        scale = self.settings.noise['scale']
        octaves = self.settings.noise['octaves']
        persistence = self.settings.noise['persistence']
        lacunarity = self.settings.noise['lacunarity']
        seed = self.settings.seed

        #Fill world array with noise values and alter with filter
        for i in range(height):
            for j in range(width):
                #fill with noise
                self.world[i][j] = noise.pnoise3(i/scale, 
                                        j/scale, 
                                        seed,
                                        octaves = octaves, 
                                        persistence = persistence, 
                                        lacunarity = lacunarity, 
                                        repeatx= width, 
                                        repeaty= height)

    def subtract_filter(self, filter_obj):
        self.world = np.subtract(self.world, 
                                    filter_obj.data * 
                                    filter_obj.weight)

    def interpolate(self):
        #Scales elements in an array to the range 0 and 1
        self.world = np.interp(self.world, 
                                (np.amin(self.world), np.amax(self.world)), 
                                (0, 1))

    def refine_world(self):
        #Adds land bias and pre-set filter
        self.world[self.world is not None] += self.settings.filters['land_bias']

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
        
        #Make new array an apply colors via boolean indexing
        self.colored_world = np.zeros(self.world.shape+(3,))

        self.colored_world[self.world < 0.28] = water_deep
        self.colored_world[(self.world >= 0.28) & (self.world < 0.38)] = water_medium 
        self.colored_world[(self.world >= 0.38) & (self.world < 0.46)] = water_shallow
        self.colored_world[(self.world >= 0.46) & (self.world < 0.48)] = sand_low
        self.colored_world[(self.world >= 0.48) & (self.world < 0.5)] = sand_high
        self.colored_world[(self.world >= 0.5) & (self.world < 0.6)] = fauna_low
        self.colored_world[(self.world >= 0.6) & (self.world < 0.7)] = fauna_medium
        self.colored_world[self.world >= 0.7] = fauna_high


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

    def save_img(self):
        ##converts array to a color image
        img = Image.fromarray((self.colored_world).astype('uint8'), 'RGB')

        ##converts to black and white
        # img_g = Image.fromarray(np.uint8(self.world * 255) , 'L')
        # img_g.show()

        # ##Image output options
        # ##shows image
        img.show()

        # ##saves as PNG file with name: "map{SEED}" to specified directory
        img.save(SCRIPT_PATH + f"\\maps\\map{self.settings.seed}.png")