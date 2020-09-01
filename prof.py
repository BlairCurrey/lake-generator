import cProfile
import pstats
import io
import os
from mapGen import *

pr = cProfile.Profile()
pr.enable()

nmap = Noisemap(width, height, scale, octaves, persistence, lacunarity, f)
print(nmap.get_stats())

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats()

with open('profiling/profile-results.txt', 'w+') as f:
    f.write(s.getvalue())