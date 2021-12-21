import copy, itertools, numpy

def pad(table, val="."):
    padded = [[val] * (len(table[0]) + 2)]
    padded.extend( [ [val, *i,val] for i in table ])
    padded.append(padded[0])
    return padded

def pad_by(table, quant):
    for i in range(quant):
        table = pad(table)
    return table

def trim(table):
    return [i[1:-1] for i in table[1:-1]]
    
def print_table(table):
    for i in table:
        if type(i)==list:
            print_table(i)
        else:
            print(i, end="")
    print("\n", end="")
    
def do_iter(table, lookup):
    # print(table)
    returner = copy.deepcopy(table)
    for row in range(len(table)):
        for col in range(len(table[row])):
            adjacent = [] 
            for ny, nx in [ (row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1), (row, col), (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)]:
                if ny < 0 or nx < 0:
                    adjacent.append(1 if lookup[0] == "#" else 0)
                elif nx >= len(table[row]) or ny >= len(table):
                    adjacent.append(1 if lookup[0] == "#" else 0)
                else:
                    adjacent.append(1 if table[ny][nx] == "#" else 0)
                    # print(table[ny][nx])
            # print(adjacent)
            joined = "".join([str(i) for i in adjacent])
            number = int(joined, 2)
            returner[row][col] = lookup[number]
            # print("coords", col, row, "got joined",joined,"binary num", number, "looked up", returner[row][col])
            
    # print(returner)
    return returner

def enhance(table, lookup, iterations=1):
    so_far = pad_by(copy.deepcopy(table), iterations*4)
    print_table(so_far)
    # so_far = do_iter(so_far)
    for i in range(iterations):
        
        so_far = do_iter(copy.deepcopy(so_far), lookup)
        padder = so_far[2][2]
        # print("padder is",padder)
        so_far = pad(pad(trim(trim(so_far)),val=padder),val=padder)
        print(numpy.count_nonzero([1 if i=="#" else 0 for i in numpy.array(so_far).flatten()]))
        # print_table(so_far)

    so_far = trim(trim(so_far))
    # print_table(so_far)
    count = numpy.count_nonzero([1 if i=="#" else 0 for i in numpy.array(so_far).flatten()])

    return count, table

