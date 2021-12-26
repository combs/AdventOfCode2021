import sys

board = []

with open("data.txt", "r") as fh:
    board = fh.readlines()
    board = [i.rstrip() for i in board]



starting_locations = {}

for row in [2, 3]:
    for col in range(len(board[row])):
        for letter in ["A", "B", "C", "D"]:
            if board[row][col]==letter:
                if letter + str(1) not in starting_locations:
                    starting_locations[letter + str(1)] = [row, col]
                else:
                    starting_locations[letter + str(2)] = [row, col]

print(starting_locations)
# we'll use Y, X indexing

desired_locations = { "A": [[3,3],[2,3]], "B": [[3,5],[2,5]], "C": [[3,7],[2,7]], "D": [[3,9],[2,9]] }
hallway_locations = [ 1, 2, 4, 6, 8, 10, 11 ]
# hallway_locations = [ [1, i] for i in hallway_locations ]
costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

def is_happy(key, locations):
    # this might just seem like it could be an "is key in desired_locations" lookup
    # but consider the case of a "cork": a letter in correct silo above a wrong letter

    letter = key[0]
    location = locations[key]
    other_same_letter = key[0] + ("2" if key[1] == "1" else "1")
    location_other = locations[other_same_letter]
    if location==desired_locations[letter][0]:
        return True
    elif location_other==desired_locations[letter][0] and location==desired_locations[letter][1]:
        return True
        
    return False

def occupied(location, locations):
    for key, val in locations.items():
        if val==location:
            return True
    return False

def get_possible_positions(key, locations):
    positions = []
    
    if is_happy(key, locations):
        return []

    [row, col] = locations[key]
    if row > 1:
        # in a silo
        if row==3:
            if occupied([2, col], locations):
                return []
        for potential in range(col, 0, -1):
            if occupied([1, potential], locations):
                break 
            if potential in hallway_locations:
                positions.append([1, potential])
        for potential in range(col, hallway_locations[-1] + 1):
            if occupied([1, potential], locations):
                break 
            if potential in hallway_locations:
                positions.append([1, potential])
    else:
        # in a hallway, want a silo
        for potential in desired_locations[key[0]]:
            if not occupied(potential, locations):
                hypothetical = locations.copy()
                hypothetical[key] = potential
                if is_happy(key, hypothetical):
                    bad = False
                    x1, x2 = col + 1, potential[1] + 1
                    for thing in range(min(x1,x2),max(x1,x2)):
                        if occupied([1, thing], hypothetical):
                            bad = True 
                    if not bad:
                        positions.append(potential)

    return positions

def get_movement_distance(location1, location2):
    x = abs(location1[1] - location2[1])
    y = abs(location1[0] - location2[0])
    return x + y

def get_cost(letter, location1, location2):
    return get_movement_distance(location1, location2) * costs[letter]

the_best = 999999999

def register_min(new):
    global the_best
    the_best = min(new, the_best)

def do_step(locations, cost=0, depth=1, moves_so_far=[]):
    global the_best
    previous_best = the_best
    best = locations.copy()
    bestcost = 999999999
    possibles = {}
    if cost > the_best:
        # print("started bust")
        return None

    for token in locations.keys():
        possibles[token] = get_possible_positions(token, locations)

    moves = sum([len(i) for i in possibles.values()])
    # print("possible moves", possibles)
    if not moves: # it's happy, or dead
        # print("out of moves")
        happy = True
        for token in locations.keys():
            happy = happy and is_happy(token, locations)
            if not happy:
                # print("unhappy", is_happy(token, locations))
                break
        if happy: # it's happy
            # print("solution found,",cost)
            return cost 
        else: # impossible
            return None
    else:
        for token, movements in sorted(possibles.items()):
            for movement in movements:
                thislocations = locations.copy()
                before = thislocations[token]

                thiscost = get_cost(token[0], thislocations[token], movement)
                if cost + thiscost > the_best:
                    # print("went bust")
                    continue
                thislocations[token] = movement

                # print("considering token",token,"movement", movement,"cost so far",cost,"new cost", thiscost)
                branch_total_cost = do_step(thislocations, cost + thiscost, depth+1, moves_so_far + [(token,movement)])
                # print("bestcost",bestcost)
                if branch_total_cost != None:
                    # print("branch total cost", branch_total_cost,"for layout", thislocations)
                    if branch_total_cost < the_best and branch_total_cost < bestcost:
                        best = thislocations
                        bestcost = branch_total_cost
                        
                        print("depth",depth,"best so far:",bestcost, "moves", moves_so_far)

    # print("best cost",bestcost)
    register_min(bestcost)
    if bestcost < previous_best:
        print(bestcost)
    return bestcost
            
for key in starting_locations:
    print(key,get_possible_positions(key, starting_locations))

            
# sys.exit(0)

print(min(the_best,do_step(starting_locations, 0)))






        
# brute force all combinations



