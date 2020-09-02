import cProfile
import pstats
import io
import os
from noisemap import noisemap
from config import config

pr = cProfile.Profile()
pr.enable()
####
SETTINGS = config()
LAKE = noisemap(SETTINGS)
###
pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats()

with open('profiling/profile-result.txt', 'w+') as f:
    f.write(s.getvalue())