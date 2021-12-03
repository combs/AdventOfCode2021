with open("data.txt", "r") as fh:
    data = list(fh.readlines())

data_parsed = []
length = len(data[0].strip())

for line in data:
    try:
        parsed = int(line.strip(), 2) # 01101 -> 13
        data_parsed.append(parsed)
    except ValueError as e:
        continue

def get_ones(ourlist):
    ones = [0] * length
    for value in ourlist:
        for bitpos in range(length):
            bit = 1 << bitpos
            index = (length - 1) - bitpos
            ones[index] += ((value & bit) > 0) # bitwise AND.
            # Some hinkiness in here because bit 0 = rightmost, but their algo wants LTR.
            # I want to store as ones[0] = bit 0, rightmost. 
            # It would be way more streamlined to just handle this as a string throughout, oops.

    return ones

def most_popular(candidates, bitpos):
    if get_ones(candidates)[bitpos] >= len(candidates)/2:
        return 1
    return 0
    
candidates_oxygen, candidates_co2 = data_parsed.copy(), data_parsed.copy()

for thing in [{"list": candidates_oxygen, "invert": False},{"list": candidates_co2, "invert": True}]:
    bitpos = 0
    candidates, invert = thing["list"], thing["invert"]

    while len(candidates) > 1:
        bit = 1 << (length - 1) - bitpos
        deleters = []
        most_pop_value = (invert ^ most_popular(candidates, bitpos)) << (length - 1) - bitpos
        # ^ is bitwise XOR, so this is saying, "get least popular if invert is True"

        for datum in candidates:
            if datum & bit != most_pop_value:
                deleters.append(datum) # can't delete from list being iterated

        for deleteme in deleters:
            if len(candidates) > 1:
                candidates.remove(deleteme)

        bitpos += 1

print(candidates_oxygen[0] * candidates_co2[0])