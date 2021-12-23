import itertools

starting_positions = []

with open("data.txt", "r") as fh:
    for line in fh.readlines():
        if "Player" not in line:
            continue
        player = line.split(" ")[1]        
        starting_positions.append(int((line.strip().split(" ")[-1])))
        

# summarize three, three-sided dice rolls 
diceroll = [0] * 10
for i in itertools.product(range(1,4), range(1,4), range(1,4)):
    diceroll[sum(i)] += 1
diceroll = tuple(diceroll)

def recurse_until_win(playerindex = 0, positions = [0, 0], scores = [0, 0], depth = 1):

    wins = [0, 0]

    if scores[0] >= 21:
        return [1, 0]
    if scores[1] >= 21:
        return [0, 1]
    
    for index in range(3,10): # 3 x 3-sided dice: 3-9 range
        new_pos = list(positions)
        new_scores = list(scores)
        new_pos[playerindex] += index
        while new_pos[playerindex] > 10:
            new_pos[playerindex] -= 10
        new_scores[playerindex] += new_pos[playerindex]
        
        result = recurse_until_win(1 - playerindex, new_pos, new_scores, depth + 1) 
        wins[0] += result[0] * diceroll[index]
        wins[1] += result[1] * diceroll[index]

    if depth < 4:
        print(depth, positions, scores, wins)
    return wins

result = recurse_until_win(0, starting_positions, [0, 0])
print(result)
print(max(result))
