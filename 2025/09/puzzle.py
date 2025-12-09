from dataclasses import dataclass
from math import sqrt
from functools import reduce

base_path = "advent-of-code-input/2025/09/" 
test_input = False
path = base_path + ("test.txt" if test_input else "input.txt")
f  = open( path)


tiles = [(int(l.split(",")[0]), int(l.split(",")[1])) for l in f.readlines()]
recangles = []

for tileId1 in range(1,len(tiles)):
    for tileId2 in range(tileId1 +1, len(tiles)):
        tile1 = tiles[tileId1]
        tile2 = tiles[tileId2]

        # 4, 7 -> 4 - 7 = -3 
        width = abs(tile1[0] - tile2[0]) + 1
        height = abs(tile1[1] - tile2[1]) +1
        recangles.append( width * height)

print("Part 1", max(recangles))