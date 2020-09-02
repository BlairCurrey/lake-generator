from configparser import ConfigParser
import os
import random as rand

class config:
    
    CONFIG_FILE = 'config.ini'
    IMG = {'x': 2048, 'y': 1024}
    SEED = rand.randint(1,100000)

    def __init__(self):
        self.parser  = ConfigParser()
        self.img = self.IMG
        self.seed = self.SEED
        self.noise = {}
        self.filters = {}
        self.init()
    
    def init(self):
        self.parser.read(self.CONFIG_FILE)
        self.load_ini()

    def load_ini(self):
        #noise
        self.noise['scale'] = self.parser.getint('noise', 'scale', fallback=200)
        self.noise['octaves'] = self.parser.getint('noise', 'octaves', fallback=5)
        self.noise['persistence'] = self.parser.getfloat('noise', 'persistence', fallback=0.5)
        self.noise['lacunarity'] = self.parser.getfloat('noise', 'lacunarity', fallback=2.0)

        # filters
        self.filters['land_bias'] = self.parser.getfloat('filters', 'land_bias', fallback=0.0)
        self.filters['path'] = self.parser.get('filters', 'path', fallback=self.get_rand_file())
        self.filters['weight'] = self.parser.getfloat('filters', 'weight', fallback=0.67)

    def get_rand_file(self):
        f = rand.choice(os.listdir("filters\\"))
        return "filters\\" + f

if __name__ == "__main__":
    c = config()
    print(c.img)