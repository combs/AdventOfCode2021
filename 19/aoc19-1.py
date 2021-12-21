import numpy, itertools, tqdm, json

scanners = []
new = []

def rotateX(x, y, z, count):
    i = count
    while i > 0:
        (x, y, z) = _rotateX(x, y, z)
        i -= 1
    return (x, y, z)

def _rotateX(x, y, z):
    return (x, -z, y)

def rotateY(x, y, z, count):
    i = count
    while i > 0:
        (x, y, z) = _rotateY(x, y, z)
        i -= 1
    return (x, y, z)

def _rotateY(x, y, z):
    return (-z, y, x)

def rotateZ(x, y, z, count):
    i = count
    while i > 0:
        (x, y, z) = _rotateZ(x, y, z)
        i -= 1
    return (x, y, z)

def _rotateZ(x, y, z):
    return (-y, x, z)

def rotate(coord, rotation):
    (x, y, z), (rotx, roty, rotz) = coord, rotation
    (x, y, z) = rotateX(x, y, z, rotx)
    (x, y, z) = rotateY(x, y, z, roty)
    (x, y, z) = rotateZ(x, y, z, rotz)

    return (x, y, z)

def offset_coord(coord, offset):
    return tuple([ coord[i] + offset[i] for i in range(3)])

with open("data.txt", "r") as fh:
    lines = fh.readlines()
    number = 0
    for line in lines:
        line = line.strip()

        # print(line)
        if "scanner" in line:
            if new:
                
                scanners.append({"coords_raw":new, "id": number})
                number = int(line.split(" scanner ")[1].split(" ")[0])
                new = []

        elif line:
            new.append(tuple([int(i) for i in line.split(",")]))
    number += 1
    scanners.append({"coords_raw":new, "id": number})

# print(scanners)

unsolved = list(range(len(scanners)))
print("yet to solve:",unsolved)

# start = unsolved.pop(0)

start = unsolved[0]
print("starting with",scanners[start]["id"])
scanners[start]["offset"] = (0,0,0)
scanners[start]["rotations"] = (0,0,0)
scanners[start]["range"] = ((-1000, 1000), (-1000, 1000), (-1000, 1000))
scanners[start]["coords_parsed"] = scanners[start]["coords_raw"].copy()
solved = []
absoluteprobes = set(scanners[start]["coords_parsed"])


while len(unsolved) > 0:

    print("solved",[i["id"] for i in solved],"unsolved",unsolved)
    candidate_index = unsolved.pop(0)
    candidate = scanners[candidate_index]
    # solved_so_far = list(solved.keys())
    candidate["matched"] = 11

    got_it = False

    # print("looking at", candidate, "vs", absoluteprobes)
    for hypothesis_matchA, hypothesis_matchB in tqdm.tqdm(itertools.product(candidate["coords_raw"],absoluteprobes)):
        # print("trying",hypothesis_matchA,"vs",hypothesis_matchB)
        for rotx, roty, rotz in itertools.product(range(4), range(4), range(4)):
            # print(rotx,roty,rotz)
            matched = 1
            offset = [ hypothesis_matchB[i] - rotate(hypothesis_matchA, (rotx, roty, rotz))[i] for i in range(3) ]
            for coord in candidate["coords_raw"]:
                it_would_be = rotate(coord, (rotx, roty, rotz))
                # print("coord",coord,"rotated to",it_would_be)
                it_would_be = offset_coord(it_would_be, offset)
                # print("coord",coord,"offset to",it_would_be)
                if tuple(it_would_be) in absoluteprobes:
                    # print("found!")
                    matched += 1
            # if matched > 1:
            #     print("offset", offset, "matched", matched)
            if matched > candidate["matched"]:
                # simplistic...
                got_it = True
                candidate["rotation"] = (rotx, roty, rotz)
                candidate["offset"] = offset
                candidate["range"] = ((-1000 + offset[0], 1000 + offset[0]),(-1000 + offset[1], 1000 + offset[1]), (-1000 + offset[2], 1000 + offset[2]))
                candidate["matched"] = matched
                parsed = []
                for i in candidate["coords_raw"]:
                    parsed.append(offset_coord(rotate(i, (rotx, roty, rotz)), offset))
                candidate["coords_parsed"] = parsed
                # print("an improved position was found:", candidate)

    if not got_it:
        unsolved.append(candidate_index)
    else:
        solved.append(candidate)
        absoluteprobes.update(candidate["coords_parsed"])
        # print("solved", candidate)
        # print("current view of all probes:", absoluteprobes)


print(len(absoluteprobes),"probes found.")

with open("probes.json", "w") as fh:
    fh.write(json.dumps(list(absoluteprobes)))

with open("scanners.json", "w") as fh:
    fh.write(json.dumps(scanners))

print("Locations:", absoluteprobes)

print("full table dump:", solved)
