from typing import Tuple, Optional, List
area = [list(l.strip()) for l in open("2024/06/input_test.txt").readlines()]

guard_chars = ["^", ">", "v", "<"]
print()
def get_guard_position(area) -> Tuple[int, int]:
    for (y_index, row) in enumerate(area):
        for (x_index, cell) in enumerate(row):
            if cell in guard_chars:
                return (y_index, x_index)

initial_y, initial_x = get_guard_position(area)
initial_guard_char  =area[initial_y][initial_x]
movement = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1,0),
    "<": (0,-1)
}
initial_movement = movement[initial_guard_char]
print(initial_y, initial_x, initial_guard_char, initial_movement )
def in_area(y,x, area): 
    return y >= 0 and x >= 0 and (y < len(area) )and (x < len(area[0]))

def rotate(y,x): 
    turn_seq = [
        (-1, 0),
        (0,1),
        (1,0),
        (0,-1)
    ]
    return turn_seq[(turn_seq.index((y,x)) +1) % len(turn_seq)]

def step_and_mark(area): 
    total_steps = 0
    y,x = (initial_y, initial_x)
    (y_movement, x_movement) = initial_movement
    while True:
        area[y][x] = "X"
        x_pos_in_front = x + x_movement
        y_pos_in_front = y + y_movement
        if not in_area(y_pos_in_front, x_pos_in_front, area):
            break
        next_field = area[y_pos_in_front][x_pos_in_front]
        if next_field == "#":
            y_movement, x_movement = rotate(y_movement, x_movement)
        x = x + x_movement
        y = y + y_movement
        total_steps += 1
    return total_steps

directional_marker = {
     (-1, 0): "^",
        (0,1): ">",
        (1,0): "v",
        (0,-1): "<"
}

def scan_ahead(area, currY, currX, currDirection) -> Optional[Tuple[int, int]]:
    y_movement, x_movement = rotate(currDirection[0], currDirection[1])
    obstacle_y = currY + currDirection[0]
    obstacle_x = currX + currDirection[1]
    obstacle_y_x = (obstacle_y, obstacle_x)
    if area[obstacle_y][obstacle_x] == "#":
        return None
    x = currX
    y = currY
    path = [(y,x)]
    positions = set([(y,x)])
    if in_area(obstacle_y, obstacle_x, area):
        if in_area(y, x, area):
            while True:
                x_pos_in_front = x + x_movement
                y_pos_in_front = y + y_movement
                if not in_area(y_pos_in_front, x_pos_in_front, area):
                    return None
                next_field = area[y_pos_in_front][x_pos_in_front]
                if next_field == "#" or (y_pos_in_front, x_pos_in_front) == obstacle_y_x :
                    y_movement, x_movement = rotate(y_movement, x_movement)
                x = x + x_movement
                y = y + y_movement
                y_x = (y, x)
                if area[y][x] == directional_marker[(y_movement, x_movement)]:
                    return obstacle_y_x
                if y_x in positions:
                    len_path = len(path)
                    last_index_y_x = len_path - 1 - path[::-1].index(y_x)
                    possible_loop = path[last_index_y_x+1:]
                    len_possible_loop = len(possible_loop)
                    path_to_y_x = path[last_index_y_x - len_possible_loop:last_index_y_x]
                    if path_to_y_x == possible_loop:
                        return obstacle_y_x
                path.append(y_x)
                positions.add(y_x)
                    
    else:
        return None



def step_and_mark_directional(area )-> List[Tuple[int,int]]:
    possible_loop = []
    y,x = (initial_y, initial_x)
    (y_movement, x_movement) = initial_movement
    finished_steps = 0
    while True:
        x_pos_in_front = x + x_movement
        y_pos_in_front = y + y_movement
        if not in_area(y_pos_in_front, x_pos_in_front, area):
            break
        next_field = area[y_pos_in_front][x_pos_in_front]
        if next_field == "#":
            y_movement, x_movement = rotate(y_movement, x_movement)
        obstacle_would_loop = scan_ahead(area, y, x, (y_movement, x_movement))
        if obstacle_would_loop:
            possible_loop.append(obstacle_would_loop)
        x = x + x_movement
        y = y + y_movement
        area[y][x] = directional_marker[(y_movement, x_movement)]
        finished_steps += 1
        print("Finished Step" + str(finished_steps) + " of " + str(total_steps))
    return possible_loop


def print_area(area):
    for row in area:
        print(row)
# print_area()
total_steps = step_and_mark([row.copy() for row in area])
possible_loops = step_and_mark_directional(area)
possible_loops = [pl for pl in possible_loops if pl != (initial_y, initial_x)]
possible_loops = set(possible_loops)
# print()
# print_area(area)
def count_steps(area):
    counter = 0
    for row in area:
        for cell in row:
            if cell == "X":
                counter += 1
    return counter
print(count_steps(area))
# print(possible_loops)
for pl in possible_loops:
    area[pl[0]][pl[1]] = "0"
# print_area(area)
print (None in possible_loops)
print(len(possible_loops))
