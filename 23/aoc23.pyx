# cython: language_level=3,infer_types=False

import sys, time
from functools import lru_cache
from operator import itemgetter, attrgetter

board = []
the_best = 999999999
steps = 0
desired_locations = { "A": ((5,3),(4,3),(3,3),(2,3)), "B": ((5,5),(4,5),(3,5),(2,5)), "C": ((5,7),(4,7),(3,7),(2,7)), "D": ((5,9),(4,9),(3,9),(2,9))}
hallway_locations = ( 1, 2, 4, 6, 8, 10, 11 )
# hallway_locations = [ [1, i] for i in hallway_locations ]
costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
starting_time = time.time()
# we'll use Y, X indexing

cpdef do_it():

    starting_locations = {}

    with open("data.sample2.txt", "r") as fh:
        board = fh.readlines()
        board = [i.rstrip() for i in board]


    for row in [2, 3, 4, 5]:
        for col in range(len(board[row])):
            for letter in ["A", "B", "C", "D"]:
                if board[row][col]==letter:
                    for i in range(4):
                        if starting_locations.get(letter + str(i), None)==None:
                            starting_locations[letter + str(i)] = (row, col)
                            break

    for key in starting_locations:
        print(key,get_possible_positions(key, starting_locations))

    print(min(the_best,do_step(starting_locations, 0)))

cdef bint is_happy(key, locations):
    cdef str letter, token
    cdef (int, int) coord, location_other, location
    
    # this might just seem like it could be an "is key in desired_locations" lookup
    # but consider the case of a "cork": a letter in correct silo above a wrong letter

    letter = key[0]
    location = locations[key]
    for location_other in desired_locations[letter]:
        if location==location_other:
            return True
        for token, coord in locations.items():
            if coord == location_other:
                if token[0] != letter:
                    return False # there is another letter below and we don't like it 
        
    return False

cdef get_possible_positions(key, dict locations):
    cdef int x1, x2, row, col, potential_row, potential_col
    cdef (int, int) potential
    cdef bint bad, impossible
    cdef list positions

    positions = []
    
    if is_happy(key, locations):
        return []

    (row, col) = locations[key]
    if row > 1:
        # in a silo
        for potential_row in range(2, row):
            if (potential_row, col) in locations.values():
                return []
        for potential_col in range(col-1, 0, -1):
            if (1, potential_col) in locations.values():
                break 
            if potential_col in hallway_locations:
                positions.append((1, potential_col))
            # 4 3 2 1 


        for potential_col in range(col+1, hallway_locations[-1] + 1):
            if (1, potential_col) in locations.values():
                break 
            if potential_col in hallway_locations:
                positions.append((1, potential_col))

            # 4 3 2 1 6 7 8 9 

        positions = list(reversed(sorted(positions, key=lambda x: abs(x[1] - col))))

        # 1 9 2 8 3 7 4 6

    else:
        # in a hallway, want a silo
        impossible = False
        for potential in desired_locations[key[0]]:
            bad = False

            for occupant, coords in locations.items():
                if coords==potential:
                    if occupant[0] != key[0]:
                        impossible = True
                        break
                        # Lower pos occupied by an interloper. bomb off
                    bad = True
            
            x1, x2 = col + 1, potential[1] + 1
            for thing in range(min(x1,x2),max(x1,x2)):
                if (1, thing) in locations.values():
                    bad = True 
            if impossible:
                break
            if not bad:
                positions.append(potential)

    return positions

cdef inline int get_movement_distance((int, int) location1, (int, int) location2):
    cdef int x, y

    x = abs(location1[1] - location2[1])
    y = abs(location1[0] - location2[0])
    return x + y

cdef inline int get_cost(letter, (int, int) location1, (int, int) location2):
    return get_movement_distance(location1, location2) * costs[letter]

cdef inline register_min(int new):
    global the_best
    the_best = min(new, the_best)

cdef do_step(locations, int cost=0, int depth=1, list moves_so_far=[]):
    global the_best, steps, starting_time
    cdef bint happy
    cdef int summed 
    cdef str token
    cdef list movements
    cdef (int, int) movement

    previous_best = the_best
    possibles = {}
    bestcost = None
    
    if cost > the_best:
        return None

    summed = 0
    
    # let's try sorting left-to-right

    for token in sorted(locations, key=lambda thing: locations[thing][1]):
        poss = get_possible_positions(token, locations)
        possibles[token] = poss
        summed += len(poss)
    
    if not summed: # it's happy, or dead
        happy = True
        for token in locations.keys():
            happy = happy and is_happy(token, locations)
            if not happy:
                break
        if happy: 
            return cost 
        else:
            return None
    else:
        for token, movements in possibles.items():
            for movement in movements:
                thiscost = get_cost(token[0], locations[token], movement)
                if cost + thiscost > the_best:
                    continue
                thislocations = locations.copy()
                thislocations[token] = movement

                branch_total_cost = do_step(thislocations, cost + thiscost, depth+1, moves_so_far + [(token,movement)])
                steps += 1
                if branch_total_cost != None:
                    
                    if branch_total_cost < the_best:
                        bestcost = branch_total_cost
                        register_min(branch_total_cost)
                        
                        print("depth",depth,"best so far:",branch_total_cost, "moves", moves_so_far)
                        print(steps / (time.time() - starting_time), "per second")


    return bestcost
    