from pathlib import Path
import numpy as np
import noise
from datetime import datetime
import json

from PIL import Image
from Filter import Filter
from Stats import Stats

PATH = Path('.').absolute()

class World:
    def __init__(self, config):
        self.config = config
        self.height_matrix = self.__get_height_matrix()
        self.height_img = self.__get_height_img()
        self.stats = Stats(self.config.elevation_range, self.height_matrix)
        self.rgb_matrix = self.__get_rgb_matrix()
        self.color_img = self.__get_color_img()

    def __get_height_matrix(self):
        # Gather releveant configurations
        noise_config = {
            "img": self.config.img,
            "noise": self.config.noise,
            "seed": self.config.seed
        }
        filter_config = self.config.filters
        
        #create and transform heightmap
        noise_matrix = self.__get_noise(noise_config)
        height_matrix = self.__get_filtered_and_constrained(noise_matrix,
                                                            filter_config)
        return height_matrix

    def __get_noise(self, config):
        #shorten config dict keys
        y = config['img']['y']
        x = config['img']['x']
        scale = config['noise']['scale']
        octaves = config['noise']['octaves']
        persistence = config['noise']['persistence']
        lacunarity = config['noise']['lacunarity']
        seed = config['seed']

        #initialize empty matrix
        noise_matrix = np.zeros((y, x))

        # Fill world matrix with noise
        # Values tend to fall 
        for i in range(y):
            for j in range(x):
                noise_matrix[i][j] = noise.pnoise3(x = i/scale, 
                                        y = j/scale, 
                                        z = seed,
                                        octaves = octaves, 
                                        persistence = persistence,
                                        lacunarity = lacunarity, 
                                        repeatx= x, 
                                        repeaty= y)
        return noise_matrix

    def __get_filtered_and_constrained(self, noise_matrix, config):
        #initialize filter and subtract from noise matrix
        filter_ = Filter(config['path'], config['weight'])
        filtered_matrix = np.subtract(noise_matrix,
                                      filter_.data * 
                                      filter_.weight)
        #Constrains values between 0-1
        constrained_matrix = np.interp(filtered_matrix, 
                                (np.amin(filtered_matrix), 
                                np.amax(filtered_matrix)),
                                (0, 1))
        #adjust if necessary
        lb = config['land_bias'] # shorten
        if lb != 0.0:
            constrained_matrix[constrained_matrix is not None] += lb

        return constrained_matrix

    def __get_rgb_matrix(self):
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
        hm = self.height_matrix # shorten
        rgb_matrix = np.zeros(hm.shape+(3,))

        rgb_matrix[hm < 0.28] = water_deep
        rgb_matrix[(hm >= 0.28) & (hm < 0.38)] = water_medium
        rgb_matrix[(hm >= 0.38) & (hm < 0.46)] = water_shallow
        rgb_matrix[(hm >= 0.46) & (hm < 0.48)] = sand_low
        rgb_matrix[(hm >= 0.48) & (hm < 0.5)] = sand_high
        rgb_matrix[(hm >= 0.5) & (hm < 0.6)] = fauna_low
        rgb_matrix[(hm >= 0.6) & (hm < 0.7)] = fauna_medium
        rgb_matrix[hm >= 0.7] = fauna_high
        
        return rgb_matrix

    def __get_color_img(self):
        return Image.fromarray((self.rgb_matrix).astype('uint8'), 'RGB')

    def __get_height_img(self):
        return Image.fromarray(np.uint8(self.height_matrix * 255) , 'L')

    def save(self):
        # Find save path
        p = self.__get_save_path()
        config = self.config.output # shorten

        if config['save_color_img']:
            self.color_img.save(p / f"{self.config.seed}.png")
        if config['save_height_img']:
            self.height_img.save(p / f"{self.config.seed}-height.png")
        if config['save_config']: 
            self.config._save_to(p / f"{self.config.seed}-config.ini")
        if config['save_stats']: 
            self.stats._save_to(p / f"{self.config.seed}-stats.json" )

    def __get_save_path(self):
        t = datetime.now().strftime("%Y_%m%d_%H%M%S")
        p = PATH / self.config.output['dir'] / f'map{t}'

        if not p.exists(): 
            p.mkdir(parents=True)

        return p