from enhancer import enhance

startingtable = []

with open("data.txt", "r") as fh:
    lookup = fh.readline().strip()
    for thing in [i.strip() for i in fh.readlines()]:
        if len(thing):
            startingtable.append(list(thing))

enhance(startingtable, lookup, 50)