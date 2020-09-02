from Noisemap import Noisemap
from Filter import Filter
from Config import Config

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
"""

if __name__ == "__main__":
    SETTINGS = Config()
    Noisemap(SETTINGS)