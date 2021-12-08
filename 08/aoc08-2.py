from segmentmess import segmentmess

(numbies, decoded_values) = segmentmess()
# only desired output: quants of #1, 4, 7, 8 digits shown
print(sum(decoded_values))