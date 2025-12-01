from functools import reduce
f = open("advent-of-code-input/2025/01/input.txt")#

turns = [(line[0], int(line[1:])) for line in f.readlines()]

# 6539 -> Too High


dial_max = 99
curr_dial = 50

zero_hit_counter = 0
zero_passed = 0

for (direction, amount) in turns:
    rotation = None
    if direction == "L":
        rotation  =  -amount
    elif direction == "R":
        rotation  = amount
    else :
        raise Exception("git gud")
    next_dial = (curr_dial + rotation) % (dial_max +1)
    zero_hit = next_dial == 0 
    if zero_hit:
        zero_hit_counter += 1
    curr_dial = next_dial
print(zero_hit_counter)
print("---------------")
curr_dial = 50
zero_passed =0
for (direction, amount) in turns:
    effective_rotation = amount % (dial_max +1)
    zeros = 0
    if direction == "L":
        if effective_rotation >= curr_dial and curr_dial != 0:
            zeros += 1
        zeros += amount // 100 # full rotation
        curr_dial = (curr_dial -amount) % (dial_max + 1)
    if direction == "R":
        if effective_rotation + curr_dial >= dial_max + 1:
           zeros += 1
        zeros += amount // 100
        curr_dial = (curr_dial + amount) % (dial_max +1)
    zero_passed += zeros
print(zero_passed)

           
