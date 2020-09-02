import Noisemap
from noisemap import noisemap
from filter_ import filter_
from config import config

if __name__ == "__main__":
    SETTINGS = config()
    LAKE = noisemap(SETTINGS)
    print(LAKE.get_stats())