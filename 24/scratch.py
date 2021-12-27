
for D03 in range(1,10):
    for D02 in range(1,10):
        for D01 in range(1,10):
            print((D02+10+(26*(D01+12)))%26 + 12)
            if D03 == ((D02+10+(26*(D01+12)))%26) + 12:
                print(D01, D02, D03)

