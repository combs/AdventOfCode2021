import numpy
coords = []
folds = []
with open("data.txt", "r") as fh:
    line = fh.readline()
    while "," in line:
        coords.append( [ int(i) for i in line.strip().split(",") ] )
        line = fh.readline()

    line = fh.readline()
    
    while "fold" in line:
        fold = line.strip().split("fold along ")[1].split("=")
        fold[1] = int(fold[1])
        folds.append( fold )
        line = fh.readline()

size = numpy.max(numpy.array(coords), axis=0)
mapped = numpy.zeros((size[1]+1, size[0]+1),dtype=numpy.uint8)

for coord in coords:
    mapped[coord[1]][coord[0]] = 1
    # numpy 2d arrays are usually y,x instead of x,y

axes = {"x": 1, "y": 0}

print(mapped)
print(folds)

merged = mapped.copy()
step = 1

for (axis, pos) in folds:
    flipped = numpy.flip(merged, axis=axes[axis])

    unflippedrange = merged.take(range(0,pos), axis=axes[axis])
    flippedrange = flipped.take(range(0,pos), axis=axes[axis])

    flippedsize = flippedrange.shape
    unflippedsize = unflippedrange.shape
    size = (max(flippedsize[0],unflippedsize[0]),max(flippedsize[1],unflippedsize[1]))

    flippedrange = numpy.pad(flippedrange, pad_width=[(0, size[0]-flippedrange.shape[0]), (0, size[1]-flippedrange.shape[1])])
    
    unflippedrange = numpy.pad(unflippedrange, pad_width=[(size[0]-unflippedrange.shape[0], 0), (size[1]-unflippedrange.shape[1], 0)])
    
    merged = flippedrange + unflippedrange

    flat = merged.copy().flatten()
    print("after fold",step,"the merged count is:",numpy.count_nonzero(flat))
    # print("MERGED")
    # print(merged)
    # print(flat)
    # print(axis,pos)
    # print(axes[axis])
    # print("UNFLIPPED")
    # print(unflippedrange)
    # print("FLIPPED")
    # print(flippedrange)
    step += 1

numpy.set_printoptions(linewidth=200)

# let's arbitrarily use "8" and "1" as our human-readable "on" and "off" for output bitmap

merged[numpy.where(merged > 1)] = 8
merged[numpy.where(merged == 0)] = 1
print(merged)

# squint!
