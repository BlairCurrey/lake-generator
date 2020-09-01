import Noisemap
from Noisemap import Noisemap
from Filter import Filter
from configreader import Config

# Image Dimensions
WIDTH = 2048
HEIGHT = 1024
CONFIG = Config()

if __name__ == "__main__":
    nmap = Noisemap(WIDTH, HEIGHT, CONFIG)
    # nmap.get_stats()