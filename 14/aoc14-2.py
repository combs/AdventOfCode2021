pairs = {}
rules = {}

from polymerize import get_atoms, parse_pairs, polymerize

with open("data.txt", "r") as fh:
    pairs = parse_pairs(fh.readline().strip())
    fh.readline()
    line = fh.readline()

    # given input:
    # # CH -> B
    # create rule:
    # CH -> CB, BH

    while " -> " in line:
        first, second = line.strip().split(" -> ")
        rules[first] = [ first[0] + second, second + first[1] ] 
        line = fh.readline()
    
# print(rules)
# print(pairs)
# print(get_atoms(pairs))
for step in range(40):
    pairs = polymerize(pairs, rules)
# print(pairs)
# print(get_atoms(pairs))

values = sorted(get_atoms(pairs).values())
# print(values)
print(values[-1] - values[0])
