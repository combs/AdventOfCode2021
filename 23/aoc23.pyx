# cython: language_level=3,infer_types=False

import sys, time
from functools import lru_cache
from operator import itemgetter, attrgetter
from multiprocessing import Manager, Queue, Process
from queue import Empty
import tqdm

board = []
the_best = 999999999
steps = 0
desired_locations_4 = { "A": ((5,3),(4,3),(3,3),(2,3)), "B": ((5,5),(4,5),(3,5),(2,5)), "C": ((5,7),(4,7),(3,7),(2,7)), "D": ((5,9),(4,9),(3,9),(2,9))}
desired_locations_2 = { "A": ((3,3),(2,3)), "B": ((3,5),(2,5)), "C": ((3,7),(2,7)), "D": ((3,9),(2,9))}
hallway_locations = ( 1, 2, 4, 6, 8, 10, 11 )
# hallway_locations = [ [1, i] for i in hallway_locations ]
costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
starting_time = time.time()
# we'll use Y, X indexing

def chunks(values, length):
    for i in range(0, len(values), length):
        yield values[i:i + length]

cpdef do_it(board):

    starting_locations = {}

    if len(board) > 6:
        rows = (2, 3, 4, 5)
    else:
        rows = (2, 3)

    for row in rows:
        for col in range(len(board[row])):
            for letter in ["A", "B", "C", "D"]:
                if board[row][col]==letter:
                    for i in range(len(rows)):
                        if starting_locations.get(letter + str(i), None)==None:
                            starting_locations[letter + str(i)] = (row, col)
                            break

    for key in starting_locations:
        print(key,get_possible_positions(key, starting_locations))

    print(the_best, do_all_steps(starting_locations, 0))

cpdef do_it_breadthwise(board):
    global steps

    starting_locations = {}

    if len(board) > 6:
        rows = (2, 3, 4, 5)
    else:
        rows = (2, 3)

    for row in rows:
        for col in range(len(board[row])):
            for letter in ["A", "B", "C", "D"]:
                if board[row][col]==letter:
                    for i in range(len(rows)):
                        if starting_locations.get(letter + str(i), None)==None:
                            starting_locations[letter + str(i)] = (row, col)
                            break

    for key in starting_locations:
        print(key,get_possible_positions(key, starting_locations))

    # universes = do_one_step(locations=starting_locations, cost=0, depth=0, moves_so_far=[], solved=False)

    next_universes = [{"locations": starting_locations, "cost": 0, "depth": 0, "solved": False}]

    while len(next_universes):
        print("considering",len(next_universes),"options, so far run", steps)
        universes = next_universes.copy() 
        next_universes = []

        for universe in universes:
            # print(universe)
            next_universes.extend(do_one_step(universe["locations"], universe["cost"], universe["depth"], universe["solved"]))
        
        for universe in next_universes:
            if universe["solved"]==True:
                solved_cost = universe["cost"]
                register_min(solved_cost)
                print("solution found", solved_cost)


cpdef do_it_parallel(board):
    cdef list next_universes, results
    cdef dict starting_locations, processes, universe
    cdef tuple rows
    cdef int row, col, i

    # global steps

    starting_locations = {}
    processes = {}

    processesToLaunch=4
    manager = Manager()
    queueFeedChildren, queueChildResults = Queue(), Queue()

    status = tqdm.tqdm()
    
    for i in range(processesToLaunch):
        processes[i] = Process(target=aoc23Runner,args=[queueFeedChildren, queueChildResults])
        processes[i].start()
        print("launched process",i)
    


    if len(board) > 6:
        rows = (2, 3, 4, 5)
    else:
        rows = (2, 3)

    for row in rows:
        for col in range(len(board[row])):
            for letter in ["A", "B", "C", "D"]:
                if board[row][col]==letter:
                    for i in range(len(rows)):
                        if starting_locations.get(letter + str(i), None)==None:
                            starting_locations[letter + str(i)] = (row, col)
                            break

    for key in starting_locations:
        print(key,get_possible_positions(key, starting_locations))

    # universes = do_one_step(locations=starting_locations, cost=0, depth=0, moves_so_far=[], solved=False)

    next_universes = [{"locations": starting_locations, "cost": 0, "depth": 0, "solved": False}]
    queueFeedChildren.put(next_universes)

    running = True
    sent = 1

    while running:
        # status.update(sent)
        try:
            results = queueChildResults.get(15)
        except Empty:
            for i in range(100):
                queueFeedChildren.put(None)
                running=False

        # print("got",len(results),"results")
        next_universes = []
        for universe in results:
            if universe["solved"]==True:
                solved_cost = universe["cost"]
                if solved_cost < the_best:
                    register_min(solved_cost)
                    print("solution found", solved_cost, "after", sent)
            else:
                if universe["cost"] < the_best:
                    next_universes.append(universe)
        
        for chunk in chunks(next_universes,100):
            queueFeedChildren.put(chunk)
        
        status.update(len(next_universes))
        sent += len(next_universes)
        del(next_universes)
        del(results)
        
        

cdef class aoc23Runner(object):
    cdef public queueFeedMe, queueSendResults

    def __init__(self, queueFeedMe, queueSendResults):
        self.queueFeedMe = queueFeedMe
        self.queueSendResults = queueSendResults
        self.run()
    
    cpdef run(self):
        cdef dict universe
        cdef list next_universes
        cdef universes

        running = True
        while running:
            universes = self.queueFeedMe.get()
            if universes==None:
                running = False
                break

            next_universes = []

            for universe in universes:
                next_universes.extend(do_one_step(universe["locations"], universe["cost"], universe["depth"], universe["solved"]))
            
            self.queueSendResults.put(next_universes)

            del(next_universes)


        
        


cdef bint is_happy(key, locations):
    cdef str letter, token
    cdef (int, int) coord, location_other, location
    
    # this might just seem like it could be an "is key in desired_locations" lookup
    # but consider the case of a "cork": a letter in correct silo above a wrong letter

    letter = key[0]
    location = locations[key]
    if "A3" in locations:
        desired = desired_locations_4
    else:
        desired = desired_locations_2

    for location_other in desired[letter]:
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

    if "A3" in locations:
        desired = desired_locations_4
    else:
        desired = desired_locations_2

    (row, col) = locations[key]
    if row > 1:
        # in a silo
        for potential_row in range(2, row):
            if (potential_row, col) in locations.values():
                return []
        for potential_col in range(col, 0, -1):
            if (1, potential_col) in locations.values():
                break 
            if potential_col in hallway_locations:
                positions.append((1, potential_col))
            # 4 3 2 1 

        for potential_col in range(col, hallway_locations[-1] + 1):
            if (1, potential_col) in locations.values():
                break
            if potential_col in hallway_locations:
                positions.append((1, potential_col))

            # 4 3 2 1 6 7 8 9 

        # 30 seconds without any re-sort
        # positions = list(reversed(sorted(positions, key=lambda x: abs(x[1] - col)))) - 88 seconds
        # positions = list(sorted(positions, key=lambda x: abs(x[1] - col))) - 36 seconds

        # 1 9 2 8 3 7 4 6

    else:
        # in a hallway, want a silo
        impossible = False

        for occupant, coords in locations.items():
            if coords in desired[key[0]]:
                if occupant[0] != key[0]:
                    impossible = True
                    break
                    # Lower pos occupied by an interloper. bomb off

        if impossible:
            return []

        for potential in desired[key[0]]:
            bad = False
            
            if col < potential[1]:
                x1 = col + 1
                x2 = potential[1] + 1
            else:
                x1 = potential[1]
                x2 = col
            
            for thing in range(x1, x2):
                if (1, thing) in locations.values():
                    bad = True 

            for thing in range(1, potential[0] + 1):
                if (thing, potential[1]) in locations.values():
                    bad = True

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


cdef do_one_step(dict locations, int cost, int depth, bint solved):

    global the_best, steps, starting_time
    cdef bint happy
    cdef int summed 
    cdef str token
    cdef list movements
    cdef (int, int) movement

    previous_best = the_best
    possibles = {}
    universes = []

    # if cost > the_best:
    #     return None

    summed = 0

    for token in sorted(locations, key=lambda thing: thing):
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
            # if cost < the_best:
            #     print("depth",depth,"best so far:",cost )
            #     print("elapsed", int(time.time() - starting_time), steps / (time.time() - starting_time), "per second")
            # register_min(cost)
            return [{"cost": cost, "locations": locations, "solved": True, "depth": depth}]
        else:
            return []
    else:
        for token, movements in possibles.items():
            for movement in movements:
                thiscost = get_cost(token[0], locations[token], movement)
                # if cost + thiscost > the_best:
                #     continue
                thislocations = locations.copy()
                thislocations[token] = movement

                universes.append({"cost": cost + thiscost, "locations": thislocations, "depth": depth + 1, "solved": False})
                # steps += 1
    # print(universes)
    return universes

cdef do_all_steps(locations, int cost=0, int depth=1, list moves_so_far=[]):
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
    
    # let's try sorting right-to-left

    # times to reach 12521 with data.sample.txt:
#    for token in sorted(locations, key=lambda thing: locations[thing][1]):  - 170 sec
#    for token in reversed(sorted(locations, key=lambda thing: locations[thing][1])): - 159 sec

    # for token in reversed(sorted(locations, key=lambda thing: thing)): - 182 sec
    # for token in sorted(locations, key=lambda thing: thing): - 106 sec
    # for token in locations: - 177 sec
    # for token in sorted(locations): - 122 sec

    for token in sorted(locations, key=lambda thing: thing):
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

                branch_total_cost = do_all_steps(thislocations, cost + thiscost, depth+1, moves_so_far + [(token,movement)])
                steps += 1
                if branch_total_cost != None:
                    if branch_total_cost < the_best:
                        bestcost = branch_total_cost
                        register_min(branch_total_cost)
                        
                        print("depth",depth,"best so far:",branch_total_cost, "moves", moves_so_far + [(token,movement)] )
                        print("elapsed", int(time.time() - starting_time), steps / (time.time() - starting_time), "per second")

    return bestcost
    