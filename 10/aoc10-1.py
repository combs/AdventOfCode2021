closers = {"[": "]", "(": ")", "{": "}", "<": ">"}
scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

score = 0
def get_opener(closer):
    for (key, val) in closers.items():
        if closer==val:
            return key
    return None

class CorruptedError(ValueError):
    myscore = 0
    def __init__(self, char):
        global score
        if char in scores:
            self.myscore = scores[char]
            score += scores[char]
    def __str__(self):
        return "CorruptedError of score " + repr(self.myscore)

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
            # if len(opened) > 0:
                # print("remaining at end of line:", opened)
        except CorruptedError as e:
            pass

print(score)