import itertools

def segmentmess():
    #  0
    # 1 2
    #  3
    # 4 5
    #  6
    
    # BTW, this is not how real 7-segment displays are numbered.
    # They go clockwise, starting at top and spiraling inward.

    # these are the allowable segment configurations, in order:

    allowednumbers = [
        [ True, True, True, False, True, True, True ],          # 0
        [ False, False, True, False, False, True, False ],      # 1
        [ True, False, True, True, True, False, True ],         # 2
        [ True, False, True, True, False, True, True ],         # 3
        [ False, True, True, True, False, True, False ],        # 4
        [ True, True, False, True, False, True, True ],         # 5
        [ True, True, False, True, True, True, True ],          # 6
        [ True, False, True, False, False, True, False ],       # 7
        [ True, True, True, True, True, True, True ],           # 8
        [ True, True, True, True, False, True, True ]           # 9
    ]

    # you could do this in a cute iterative way, or ...
    orders = ["a", "b", "c", "d", "e", "f", "g"]

    # keep track of ultimately decoded values, later
    numbies = [0] * 10
    decoded_values = []

    with open("data.txt", "r") as fh:

        for line in fh.readlines():

            # this could be reduced to fewer lines, but readability

            (ciphered_patterns, ciphered_values) = line.split("|")
            ciphered_patterns_booleans, ciphered_values_booleans = [], []
            ciphered_patterns = ciphered_patterns.strip().split(" ")
            ciphered_values = ciphered_values.strip().split(" ")
            
            # convert to "abd" to [ True, True, False, etc ] to show whether each segment is present 
            # in the displayed values
            
            for digit in ciphered_patterns:
                ciphered_patterns_booleans.append([ segment in digit for segment in orders ])

            for digit in ciphered_values:
                ciphered_values_booleans.append([ segment in digit for segment in orders ])
                
            for transmutation in itertools.permutations(list(range(7))):

                # transmutation contains desired order of segments, like ( 3, 4, 1, 5, 6, 0, 2)
                
                good = True

                for digit in ciphered_patterns_booleans:

                    # we use this hypothesis to transmute each digit

                    transmuted = [ digit[pos] for pos in transmutation ]
                    
                    # if this results in an invalid segment configuration, we disqualify the hypo

                    if transmuted not in allowednumbers:
                        good = False # is there a double-break? lol
                        break 

                if good==True:
                    print("hypothesis:",transmutation, "for ciphered values:",ciphered_values)
                    val = ""
                    for digit in ciphered_values_booleans:
                        transmuted = [ digit[pos] for pos in transmutation ]
                        decoded = allowednumbers.index(transmuted)
                        val += str(decoded)
                        numbies[decoded] += 1
                    print("decoded entire value:",val)
                    decoded_values.append(int(val))
                    
    return (numbies, decoded_values)