import pstats

p = pstats.Stats('stats.txt')
p.sort_stats('time').print_stats(20)