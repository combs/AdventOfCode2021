import json, itertools

with open("scanners.json", "r") as fh:
    scanners = json.load(fh)

absolutescanners = [i["offset"] for i in scanners]

max_val = 0

for a, b in itertools.combinations(absolutescanners, 2):
    (x, y, z) = [ abs(a[i] - b[i]) for i in range(3)]
    manhattan_distance = sum([x, y, z])
    max_val = max(max_val, manhattan_distance)

print(max_val)