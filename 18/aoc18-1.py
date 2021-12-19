import json

def get_greatest_value(tree):
    max_val = 0
    for item in tree:
            
        if type(item)==int:
            max_val = max(max_val, item)
        else:
            max_val = max(max_val, get_greatest_value(item))

    return max_val
            
def get_greatest_depth(tree, depth=1):
    max_depth = depth
    for item in tree:
        if type(item) == list:
            max_depth = max(depth, get_greatest_depth(item, depth + 1))
    return max_depth

def split_first(tree):
    # print("split? considering ",tree)
    if type(tree)==int:
        item = tree
        if item >= 10:
            left = int(item / 2.0)
            right = item - left
            print("split",tree,"new vals",(left,right))
            return ([left, right], True)
    else:
        for index, item in enumerate(tree.copy()):
            if type(item) == list:
                tree[index], changed = split_first(item)
                if changed: 
                    return (tree, True)
            elif item >= 10:
                left = int(item / 2.0)
                right = item - left
                tree[index] = [left, right]
                print("split",tree,"new vals",(left,right))
                return (tree, True)

    return tree, False

def explode_first(tree, cursor=[0]):
    ourcursor = cursor.copy()
    # print("explode? considering",tree,"cursor",cursor, "cursor length",len(cursor))

    thing = get_pos(tree, cursor)
    if type(thing)==list:
        if len(cursor) >= 4:
            current_val = thing
            print("exploding thing",thing,"at location",cursor)
            if len(thing) > 2:
                raise ValueError("Trying to explode >2 items")
            left = find_neighbor_left(tree, cursor + [0])
            right = find_neighbor_right(tree, cursor + [1])
            replacement = []
            if left != None:
                leftval = get_pos(tree, left)
                print("Found left neighbor",left,"leftval",leftval)
                set_pos(tree, left, leftval + current_val[0])
            
            if right != None:
                rightval = get_pos(tree, right)
                print("Found right neighbor",right,"rightval",rightval)
                set_pos(tree, right, rightval + current_val[1])
            
            # tree.remove(thing)
            set_pos(tree, cursor, 0)

            print("exploded a thing. final tree", tree)
            return (tree, True)
        else:
            # print("cursor wasn't long enuff")
            for index, item in enumerate(thing):
                (tree, did_something) = explode_first(tree, cursor + [ index ] )
                if did_something:
                    # print("did something in child call")
                    return (tree, True)
    
    return (tree, False)
        

def get_pos(tree, target):
    # print("get_pos",tree,target)
    indices = target.copy()
    if (type(tree)==int) and target==[0]:
        return tree
    item = tree.copy()

    while len(indices):
        item = item[ indices.pop(0) ]
    return item

def set_pos(tree, target, val):
    item = tree
    indices = target.copy()
    while len(indices) > 1:
        item = item[ indices.pop(0) ]
    item[indices[0]] = val
    return tree

def find_neighbor_left(tree, target):
    # pass in [0, 1, 2] to specify third child of second child of first child
    depth = len(target) - 1
    cursor = list(target)
    while depth > -1:
        # print("The tree is",tree,"depth is",depth,"cursor is",cursor)
        cursor[depth] -= 1
        thing = None
        if cursor[depth] == -1:
            # print("Walking up a level")
            cursor[depth] += 1
            depth -= 1
            cursor.pop()
            continue

        try:
            thing = get_pos(tree, cursor)
            # print("The new thing is", thing)
        except TypeError:
            print("found an int? up one more level")
            cursor[depth] += 1
            depth -= 1
            cursor.pop()
            continue
        except ValueError:
            print("got ValueError")
            continue
        except IndexError:
            print("IndexError, why?")
            
            continue
        
        if type(thing) == list:
            # recurse into it... somehow
            # print("recurse! cursor is", cursor, "length of cursor is",len(cursor),"and greatest depth is",get_greatest_depth(tree))

            cursor += [ len(thing) ] # start at rightmost pos of new branch 
            # we will take off 1 at beginning of next loop
            # print("appended to cursor")
            # print("new cursor", cursor)
            depth += 1

        else:
            # print("left neighbor found", cursor)
            return cursor
    return None


def find_neighbor_right(tree, target):
    # pass in [0, 1, 2] to specify third child of second child of first child
    depth = len(target) - 1
    cursor = list(target)
    while depth > -1:
        # print("The tree is",tree,"depth is",depth,"cursor is",cursor)
        cursor[depth] += 1
        thing = None

        try:
            thing = get_pos(tree, cursor)
            # print("The new thing is", thing)
        except ValueError:
            # print("got ValueError")
            continue
        except TypeError as e:
            # print("found an int? up one more level", e)
            cursor[depth] = 0
            depth -= 1
            cursor.pop()
            continue
        except IndexError:
            # print("IndexError, overflowed? Walking up a level")
            cursor[depth] = 0
            depth -= 1
            cursor.pop()
            continue


        if type(thing) == list:
            # recurse into it... somehow
            # print("recurse! cursor is", cursor, "length of cursor is",len(cursor),"and greatest depth is",get_greatest_depth(tree))

            # if cursor[depth] == len(thing):
            #     print("Walking up a level")
            #     cursor[depth] -= 1
            #     depth -= 1
            #     continue

            cursor += [ -1 ] # start at leftmost pos of new branch
            # print("appended to cursor")
            # print("new cursor", cursor)
            depth += 1

        else:
            print("right neighbor found", cursor)
            return cursor
    return None




        



def process_snailfish(snailfish_additions):

    snailfish = snailfish_additions.pop(0)

    while len(snailfish_additions):

        print("snailfish before", snailfish)
        snailfish = [ snailfish, snailfish_additions.pop(0) ]

        print("snailfish after addition", snailfish)

        did_something = True

    # while (get_greatest_depth(snailfish) > 4) or (get_greatest_value(snailfish) > 9):

        while did_something == True:
            snailfish, did_something = explode_first(snailfish)
            if did_something:
                print("did an explode")
                continue
            snailfish, did_something = split_first(snailfish)
            if did_something:
                print("did a split")
                continue
        

    # while greatest_depth > 4 or any_val > 10
    #  check for depth > 4
    #   if yes, explode leftmost
    #  else, check for any val > 10
    #   if yes, split leftmost
    # then, item has been reduced. 

    # for item in datum:
    #     if type(item) == int:
    #         if depth <= 4:
    #             if item > 9:
    #                 item = split(item)
    #         else:
    #             item = explode(item)
    # print(find_neighbor_left(snailfish, [1]))
    # print(find_neighbor_right(snailfish, [0]))
    # print(get_greatest_depth(snailfish), get_greatest_value(snailfish))

    print("final result", snailfish)


with open("data.sample.txt", "r") as fh:
    lines = fh.readlines()

data = []
for line in lines:
    data.append(json.loads(line))
    # print()

# print(set_pos( [ [ [ 3, 3], [2, 2]], [4, 4]], [0,0,0] , 17))
process_snailfish(data)