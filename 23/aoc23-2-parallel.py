import pyximport
pyximport.install()

from aoc23 import do_it_parallel

with open("data.sample2.txt", "r") as fh:
    board = fh.readlines()
    board = [i.rstrip() for i in board]

do_it_parallel(board)
