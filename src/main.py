from World import World
from Filter import Filter
from Config import Config

if __name__ == "__main__":
    CONFIG = Config()
    w = World(CONFIG)
    print(w.stats.elevation)
    w.color_img.show()
    w.height_img.show()
    w.save()