from dataclasses import dataclass
from math import sqrt
from functools import reduce

base_path = "advent-of-code-input/2025/09/" 
test_input = False
path = base_path + ("test.txt" if test_input else "input.txt")
f  = open( path)

tiles = [(int(l.split(",")[0]), int(l.split(",")[1])) for l in f.readlines()]
rectangles = []
for tileId1 in range(1,len(tiles)):
    for tileId2 in range(tileId1 +1, len(tiles)):
        tile1 = tiles[tileId1]
        tile2 = tiles[tileId2]
        width = abs(tile1[0] - tile2[0]) + 1
        height = abs(tile1[1] - tile2[1]) +1
        rectangles.append( width * height)

print("Part 1", max(rectangles))

# Solution Part 2:
# Connect all Red Tiles
# Depth First Search to get inner area
# For each row of the input grid, create a set (or set of spans) of tiles that are not part of green and red 
# find largest rectangles, sort descending
# iterate until one is found, that has no coordinates not in area.
#   how to check: for each row the rectangle spans, check  if it cells overlap with the spans of "forbidden" cells

