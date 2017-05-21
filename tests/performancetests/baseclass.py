# source: https://stackoverflow.com/questions/8494358/defining-repr-when-subclassing-set-in-python
# I think I have something that gets you what you want, in addition to showing some benchmarks. They are almost all equivalent though I am sure there is a difference in memory usage.
# def timeit(exp, repeat=10000):
#     results = []
#     for _ in xrange(repeat):
#         start = time.time()
#         exec(exp)
#         end = time.time()-start
#         results.append(end*1000)
#     return sum(results) / len(results)


# Results:

# Alpha(): 0.0287627220154

# Alpha2(): 0.0286467552185

# Alpha3(): 0.0285225152969