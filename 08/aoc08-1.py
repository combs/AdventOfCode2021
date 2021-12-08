from segmentmess import segmentmess

(numbies, decoded_values) = segmentmess()
# only desired output: quants of #1, 4, 7, 8 digits shown
print(sum((numbies[1],numbies[4],numbies[7],numbies[8])))