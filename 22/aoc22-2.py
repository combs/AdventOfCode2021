
import numpy, re, itertools, tqdm
from tqdm.contrib.itertools import product

rules = []
total = 0
xcalc, ycalc, zcalc = [], [], []
xvals, yvals, zvals = set(), set(), set()

with open("data.txt", "r") as fh:
    for line in fh.readlines():
        if line.strip():
            expression = r".*x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+).*"
            match = re.match(expression, line)
            if match:
                newrule = [line.split(" ")[0]=="on"] + [ int(i) for i in match.groups() ]
                rules.append(newrule)

print(rules)

# we compile all the min and max on each axis for each rule

for i in rules:
    xvals.update([i[1], i[2], i[2] + 1])
    yvals.update([i[3], i[4], i[4] + 1])
    zvals.update([i[5], i[6], i[6] + 1])

# this is so that we can make a sparse table where a single bool represents the entire rect
#
# each bool will represent the space between adjacent edges
# for sample edge vals [1, 10, 100]:
# False, True
# represents [1:10] being False and [10:100] being True
#
# by including all rule values we allow for later rectangle intersections (checkerboard type)
#
# we double up the lists so that we can account for the edge case of a [1, 1] box

xvals = sorted(list(xvals)) 
xvals += [xvals[-1]]
yvals = sorted(list(yvals)) 
yvals += [yvals[-1]]
zvals = sorted(list(zvals))
zvals += [zvals[-1]]

# print("xvals", xvals, "yvals", yvals, "zvals", zvals)

for x in range(len(xvals) - 1):
    xcalc.append(xvals[x+1] - xvals[x])
for y in range(len(yvals) - 1):
    ycalc.append(yvals[y+1] - yvals[y])
for z in range(len(zvals) - 1):
    zcalc.append(zvals[z+1] - zvals[z])

xcalc, ycalc, zcalc = tuple(xcalc), tuple(ycalc), tuple(zcalc)
# print("xcalc", xcalc, "ycalc", ycalc, "zcalc", zcalc)

table = numpy.zeros((len(xvals), len(yvals), len(zvals)), dtype=numpy.bool)

for rule in tqdm.tqdm(rules):
    
    # We break it down to a table of "spaces between values"
    xindices = [ xvals.index(rule[1]), xvals.index(rule[2] ) ]
    yindices = [ yvals.index(rule[3]), yvals.index(rule[4] ) ]
    zindices = [ zvals.index(rule[5]), zvals.index(rule[6] ) ]
    # print("RULE",rule)
    # print("indices x", xindices[0], ":", xindices[1]+1, ", y", yindices[0], ":", yindices[1]+1, ", z", zindices[0], ":", zindices[1]+1)
    table[xindices[0]:xindices[1]+1, yindices[0]:yindices[1]+1, zindices[0]:zindices[1]+1] = rule[0]
    # print("delta", numpy.count_nonzero(table) - previous)

for (x, y, z) in tqdm.tqdm(numpy.argwhere(table)):
    total += xcalc[x] * ycalc[y] * zcalc[z] 

print(total)
