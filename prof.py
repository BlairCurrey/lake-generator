import cProfile
import pstats
import io
import os
from Noisemap import Noisemap
from Config import Config

pr = cProfile.Profile()
pr.enable()
####
SETTINGS = Config()
Noisemap(SETTINGS)
###
pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats()

with open('profiling/profile-result.txt', 'w+') as f:
    f.write(s.getvalue())