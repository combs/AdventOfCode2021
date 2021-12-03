with open("data.txt", "r") as fh:
    data = list(fh.readlines())

length = len(data[0].strip())
ones = [0] * length
count = 0

for line in data:
    try:
        parsed = int(line.strip(), 2) # 01101 -> 13
        # print(line.strip(), parsed)
        for bitpos in range(length):
            bit = 1 << bitpos
            index = (length - 1) - bitpos
            ones[index] += ((parsed & bit) > 0) # bitwise AND.
        count += 1
    except ValueError as e:
        continue

# print(ones)
gamma, epsilon = 0, 0

for bitpos in range(length):
    if ones[bitpos] > (count / 2):
        gamma = gamma | (1 << (length - 1) - bitpos)
    else:
        epsilon = epsilon | (1 << (length - 1) - bitpos)

output = gamma * epsilon

# print(gamma, epsilon, output)
print(output)