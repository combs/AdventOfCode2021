closers = {"[": "]", "(": ")", "{": "}", "<": ">"}
scores_incomplete = {"(": 1, "[": 2, "{": 3, "<": 4}
incompletescores = []

def get_opener(closer):
    for (key, val) in closers.items():
        if closer==val:
            return key
    return None

class CorruptedError(ValueError):
    def __str__(self):
        return "CorruptedError"

with open("data.txt", "r") as fh:
    for line in fh.readlines():
        try:
            opened = []
            for char in line.strip():
                if char in closers: # is it a valid opening char?
                    opened.append(char)
                elif char in closers.values():
                    if opened[-1] == get_opener(char): # is it the closer for most recent opened?
                        opened.pop()
                    else:
                        raise CorruptedError(char)
                        # A corrupted line was found
                else:
                    raise ValueError("A strange character was found")
            if len(opened) > 0:
                linescore = 0 
                for char in reversed(opened):
                    linescore *= 5
                    linescore += scores_incomplete[char]
                incompletescores.append(linescore)
                
        except CorruptedError as e:
            pass

index = int(len(incompletescores)/2) # halve it... 
# always odd, so say len 7, 7/2 -> 3.5 -> 3. 
# index 3 in zero-indexed 0-6 array has 3 before and 3 after, so it is the middle

print (sorted(incompletescores)[index])