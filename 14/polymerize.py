
start, end = "s", "e"

def get_atoms(pairs):

    quants = {}
    letters = set(sorted("".join(pairs.keys())))
    letters.remove(start)
    letters.remove(end)

    for letter in letters:
        quant = 0
        for pair in pairs:
            if pair[0]==letter:
                quant += pairs[pair]
            # elif pair[0]==start:
            #     quant += pairs[pair]
            if pair[1]==letter:
                quant += pairs[pair]
            # elif pair[1]==end:
            #     quant += pairs[pair]
            
            # if letter in pair:
            #     if ((start in pair) or (end in pair)) and (pairs[pair] > 0):
            #         quant += 1
            #         print(letter, quant)

        quants[letter] = quant / 2

    return quants

def parse_pairs(string):
    returner = {}
    # use magic tokens for start and end of sequence
    for pair in [ start + string[0], string[-1] + end ]:
        returner[pair] = 1

    for i in range(len(string)-1):
        pair = string[i:i+2]
        returner[pair] = returner.get(pair, 0) + 1

    return returner

def polymerize(pairs, rules):

    newpairs = dict(pairs)
    # print(pairs)
    for pair in pairs:
        if pair in rules:
            quant = pairs[pair]
            outcomes = rules[pair]
            newpairs[pair] = newpairs.get(pair, 0) - quant
            for outcome in outcomes:
                # print(quant,"count of",pair,"becomes",outcome)
                newpairs[outcome] = newpairs.get(outcome, 0) + quant
            # print(newpairs)
    
    return newpairs
