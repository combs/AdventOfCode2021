import numpy
from scipy import ndimage

with open("data.txt", "r") as fh:
    lines = fh.readlines()

heightmap = []
for line in lines:
    row = [ int(i) for i in line.strip() ] 
    heightmap.append(row)

heightmap = numpy.array(heightmap)

# I thiiiink we only really care about finding the 9-height lines and getting 
# the contiguous regions between them.

labels, poo = ndimage.label(heightmap != 9)

# after this step, we have a map of labeled, numbered, contiguous areas, like this:
# [[1 1 0 0 0 2 2 2 2 2]
#  [1 0 3 3 3 0 2 0 2 2]
#  [0 3 3 3 3 3 0 4 0 2]
#  [3 3 3 3 3 0 4 4 4 0]
#  [0 3 0 0 0 4 4 4 4 4]] 

# Count the number of each int value in the above map.
sizes = sorted(numpy.bincount(labels.flatten())[1:]) # Throw away the count of 0s, we don't care.

print (sizes[-1] * sizes[-2] * sizes[-3])
