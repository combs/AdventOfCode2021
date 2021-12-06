import numpy
from tqdm import tqdm

cdef class aoc06cython(object):
    def __init__(self):
        self.doit()
    
    cdef public void doit(self):
        with open("data.txt", "r") as fh:
            dataline = fh.read()
            ages = dataline.strip().split(",")
            ages = [int(a) for a in ages]
                
        fishes = numpy.array(ages, dtype=numpy.int8)

        for day in tqdm(range(256), desc="Fish stuff..."):
            # print( day, fishes)
            fishes -= 1
            newbies = numpy.count_nonzero(numpy.where(fishes == -1))
            fishes = numpy.append(fishes, [8] * newbies)
            numpy.add(fishes, 7, out=fishes, where=fishes == -1)

        print(fishes.shape[0])