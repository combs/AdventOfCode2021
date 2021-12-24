
import numpy, re

rules = []
xrange = yrange = zrange = 101
xoffset = yoffset = zoffset = 50

with open("data.txt", "r") as fh:
    for line in fh.readlines():
        if line.strip():
            expression = r".*x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+).*"
            match = re.match(expression, line)
            if match:
                newrule = [line.split(" ")[0]=="on"] + [ int(i) for i in match.groups() ]
                rules.append(newrule)
    
def apply_rule(table, value, xmin, xmax, ymin, ymax, zmin, zmax, ranges, offsets):
    
    xmin = max(0, xmin+offsets[0])
    xmax = min(ranges[0], xmax + offsets[0] + 1)
    ymin = max(0, ymin+offsets[1])
    ymax = min(ranges[1], ymax + offsets[1] + 1)
    zmin = max(0, zmin+offsets[2])
    zmax = min(ranges[2], zmax + offsets[2] + 1)
    table[xmin:xmax, ymin:ymax, zmin:zmax] = value
    return table


print(rules)

table = numpy.zeros((xrange, yrange, zrange),dtype=numpy.bool)
ranges = (xrange, yrange, zrange)
offsets = (xoffset, yoffset, zoffset)

for rule in rules:
    table = apply_rule(table, *rule, ranges, offsets)
    # print(table)
    print(numpy.count_nonzero(table))

