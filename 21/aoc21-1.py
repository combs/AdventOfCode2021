players = {}
scores = {}
winner = None

with open("data.txt", "r") as fh:
    for line in fh.readlines():
        if "Player" not in line:
            continue
        player = line.split(" ")[1]        
        players[player] = int(line.strip().split(" ")[-1])
        scores[player] = 0

def deterministic_die():
    thing = 1
    while True:
        yield thing
        thing += 1
        if thing > 100:
            thing=1

def whose_turn_is_it_anyways(players, starting="1"):
    index = players.index(starting)
    while True:
        yield players[index]
        index += 1
        try:
            players[index]
        except IndexError:
            index=0
        



dd = deterministic_die()
who = whose_turn_is_it_anyways(sorted(list(players.keys())), "1")
rolls = 0

while winner==None:
    player = next(who)
    roll = []
    for i in range(3):
        roll.append(next(dd))
        rolls += 1
    roll = sum(roll)
    pos = players[player]
    pos += roll
    while pos > 10:
        pos -= 10
    scores[player] += pos
    players[player] = pos

    if scores[player] >= 1000:
        winner = player

print(players, scores)
loser = next(who)
print(scores[loser],rolls)
print(scores[loser] * rolls)