from configparser import ConfigParser
import os
from pathlib import Path
import random as rand

"""
Description of available settings in `config.ini`:
        [dir]:          directory related settings
        map_output:     relative path to output images to
        filters:        

        [noise]         noise related settings
        scale:
        octaves:
        persistence:
        lacunarity:

        [filters]       filter and post-processing settings
        land_bias:
        path:           Empty or ommitted will result in a random choice which 
                        is recommended if you are generating lots of images and 
                        want variety.

                        Relative directory to desired filter. This filter is 
                        subtracted from the heigthmap after it is generated 
                        with noise.
        
        weight:         A multiplier to control how much effect the filter has.

        [output]
        show = True
        dir = maps/
        save_config = True
        save_stats = True
"""

class Config:
    
    CONFIG_FILE = 'src/config.ini'
    IMG = {'x': 2048, 'y': 1024}
    SEED = rand.randint(1,100000)

    def __init__(self):
        self.parser = ConfigParser()
        self.img = self.IMG
        self.seed = self.SEED
        self.noise = {}
        self.filters = {}
        self.output = {}
        self.init()
    
    def init(self):
        self.parser.read(self.CONFIG_FILE)
        self.load_ini()

    def load_ini(self):
        # noise
        self.noise['scale'] = self.parser.getint('noise', 'scale', fallback=200)
        self.noise['octaves'] = self.parser.getint('noise', 'octaves', fallback=5)
        self.noise['persistence'] = self.parser.getfloat('noise', 'persistence', fallback=0.5)
        self.noise['lacunarity'] = self.parser.getfloat('noise', 'lacunarity', fallback=2.0)

        # filters
        self.filters['land_bias'] = self.parser.getfloat('filters', 'land_bias', fallback=0.0)
        self.filters['path'] = self.parser.get('filters', 'path', fallback=self.get_rand_file())
        self.filters['weight'] = self.parser.getfloat('filters', 'weight', fallback=0.67)

        # output
        self.output['show'] = self.parser.getboolean('output', 'show', fallback=True)
        self.output['dir'] = self.parser.get('output', 'dir', fallback="maps")
        self.output['save_config'] = self.parser.getboolean('output', 'save_config', fallback=True)
        self.output['save_stats'] = self.parser.getboolean('output', 'save_stats', fallback=True)

    def get_rand_file(self):
        f = rand.choice(os.listdir("filters\\"))
        return "filters\\" + f

    def save_to(self, path):
        with open(f'{path}', 'w') as f:
            self.parser.write(f)

if __name__ == "__main__":
    c = Config()
    print(c.output['show'])