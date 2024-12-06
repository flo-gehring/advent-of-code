from typing import Tuple, List
area = [list(l.strip()) for l in open("2024/06/input.txt").readlines()]

guard_chars = ["^", ">", "v", "<"]
print()
def get_guard_position() -> Tuple[int, int]:
    for (y_index, row) in enumerate(area):
        for (x_index, cell) in enumerate(row):
            if cell in guard_chars:
                return (y_index, x_index)

initial_y, initial_x = get_guard_position()
initial_guard_char  =area[initial_y][initial_x]
movement = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1,0),
    "<": (0,-1)
}
initial_movement = movement[initial_guard_char]
print(initial_y, initial_x, initial_guard_char, initial_movement )
def in_area(y,x): 
    return y >= 0 and x >= 0 and (y < len(area) )and (x < len(area[0]))

def rotate(y,x): 
    turn_seq = [
        (-1, 0),
        (0,1),
        (1,0),
        (0,-1)
    ]
    return turn_seq[(turn_seq.index((y,x)) +1) % len(turn_seq)]

def step_and_mark( ): 
    y,x = (initial_y, initial_x)
    (y_movement, x_movement) = initial_movement
    while True:
        area[y][x] = "X"
        x_pos_in_front = x + x_movement
        y_pos_in_front = y + y_movement
        if not in_area(y_pos_in_front, x_pos_in_front):
            break
        next_field = area[y_pos_in_front][x_pos_in_front]
        if next_field == "#":
            y_movement, x_movement = rotate(y_movement, x_movement)
        x = x + x_movement
        y = y + y_movement


def print_area():
    for row in area:
        print(row)
# print_area()
step_and_mark()
# print()
# print_area()
def count_steps():
    counter = 0
    for row in area:
        for cell in row:
            if cell == "X":
                counter += 1
    return counter
print(count_steps())
    
