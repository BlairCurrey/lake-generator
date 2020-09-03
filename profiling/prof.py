import cProfile
import pstats
import io
import os
from World import World
from Config import Config

pr = cProfile.Profile()
pr.enable()
####
CONFIG = Config()
w = World(CONFIG)
w.color_img.show()
w.save()
###
pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats()

with open('profiling/profile-result.txt', 'w+') as f:
    f.write(s.getvalue())