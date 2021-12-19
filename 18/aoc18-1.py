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
            # print("split",tree,"new vals",(left,right))
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
                # print("split",tree,"new vals",(left,right))
                return (tree, True)

    return tree, False

def explode_first(tree, cursor=[]):
    ourcursor = cursor.copy()
    # print("explode? considering",tree,"cursor",cursor, "cursor length",len(cursor))
    if len(cursor)==0:
        thing = tree
    else:
        thing = get_pos(tree, cursor)
    # print("looking at", thing)
    if type(thing) != int:
        
        for index, item in enumerate(thing):
            # print("considering",item,"inside explode")
            (tree, did_something) = explode_first(tree, cursor + [ index ] )
            if did_something:
                
                return (tree, True)
            
            if (len(cursor) >= 4) and len(thing) > 1 and (type(thing[0])==int and type(thing[1])==int):
                
                # print("exploding thing",thing,"at location",cursor)
                if len(thing) > 2:
                    raise ValueError("Trying to explode >2 items")

                left = get_neighbor_left(tree, cursor + [0])
                if left != None:
                    leftval = get_pos(tree, left)
                    # print("Found left neighbor",left,"leftval",leftval)
                    set_pos(tree, left, leftval + thing[0])
                
                right = get_neighbor_right(tree, cursor + [1])
                if right != None:
                    rightval = get_pos(tree, right)
                    # print("Found right neighbor",right,"rightval",rightval)
                    set_pos(tree, right, rightval + thing[1])
                
                set_pos(tree, cursor, 0)

                # print("exploded a thing. final tree", tree)
                return (tree, True)
    # else:
    #     right = get_neighbor_right(tree, cursor)
    #     print("found right neighbor", right)
    #     if right != None:
    #         print("trying to iterate into", right)
    #         (tree, did_something) = explode_first(tree, right )
    #         if did_something:
    #             # print("did something in child call")
    #             return (tree, True)
    
    return (tree, False)
        

def get_pos(tree, target):
    # print("get_pos",tree,target)
    indices = target.copy()
    if (type(tree)==int) and (target==[0]):
        return tree
    item = tree.copy()

    while len(indices):
        item = item[ indices.pop(0) ]
    # print("got item",item)
    return item

def set_pos(tree, target, val):
    item = tree
    indices = target.copy()
    while len(indices) > 1:
        item = item[ indices.pop(0) ]
    item[indices[0]] = val
    return tree

def get_neighbor_left(tree, target):
    # pass in [0, 1, 2] to specify third child of second child of first child
    depth = len(target) - 1
    cursor = list(target)
    while depth > -1:
        # print("The tree is",tree,"depth is",depth,"cursor is",cursor)
        cursor[depth] -= 1
        thing = None
        if cursor[depth] == -1:
            # print("Walking up a level")
            depth -= 1
            cursor.pop()
            continue

        try:
            thing = get_pos(tree, cursor)
            # print("The new thing is", thing)
        except TypeError:
            # print("found an int? up one more level")
            depth -= 1
            cursor.pop()
            continue
        except ValueError:
            # print("got ValueError")
            continue
        except IndexError:
            # print("IndexError, why?")
            
            continue
        
        if type(thing) == list:
            # print("recurse! cursor is", cursor, "length of cursor is",len(cursor),"and greatest depth is",get_greatest_depth(tree))

            cursor += [ len(thing) ] # start at rightmost pos of new branch 
            # we will take off 1 at beginning of next loop
            # print("appended to cursor")
            # print("new cursor", cursor)
            depth += 1

        else:
            # print("left neighbor found", cursor, "val", thing)
            return cursor
    return None


def get_neighbor_right(tree, target):
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
            # print("right neighbor found", cursor, "val", thing)
            return cursor
    return None

# [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[7, 7], [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]]

def get_first_int(tree):
    if type(tree[0]) != int:
        get_first_int(tree[0])
    return tree[0]

def get_last_int(tree):
    if type(tree[-1]) != int:
        get_first_int(tree[-1])
    return tree[-1]

def multiply_pairs(tree, left, right):
    leftval = tree[0]
    rightval = tree[1]

    if type(tree[0])==list:
        leftval = multiply_pairs(tree[0], left, right)
        
    if type(tree[1])==list:
        rightval = multiply_pairs(tree[1], left, right)
    
    return (leftval * left) + (rightval * right)

def process_magnitude(snailfish):
    return (multiply_pairs(snailfish, 3, 2))



def process_snailfish(snailfish_additions):

    snailfish = None

    while len(snailfish_additions):

        print("snailfish before", snailfish)
        if not snailfish:
            snailfish = snailfish_additions.pop(0)
        else:
            snailfish = [ snailfish, snailfish_additions.pop(0) ]

        print("SNAILFISH AFTER ADDITION", snailfish)

        did_something = True

    # while (get_greatest_depth(snailfish) > 4) or (get_greatest_value(snailfish) > 9):

        while did_something == True:
            snailfish, did_something = explode_first(snailfish)
            if did_something:
                print("did an explode", snailfish)
            else:
                snailfish, did_something = split_first(snailfish)
                if did_something:
                    print("did a split", snailfish)
        
        print("SNAILFISH AFTER OPERATIONS:", snailfish)

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
    # print(get_neighbor_left(snailfish, [1]))
    # print(get_neighbor_right(snailfish, [0]))
    # print(get_greatest_depth(snailfish), get_greatest_value(snailfish))

    print("final result", snailfish)
    print("magnitude", process_magnitude(snailfish))


with open("data.txt", "r") as fh:
    lines = fh.readlines()

data = []
for line in lines:
    data.append(json.loads(line))
    
process_snailfish(data)