from typing import Tuple, Optional, List
test = False
path = "2024/06/input_test.txt" if test else "2024/06/input.txt"
input_area = [list(l.strip()) for l in open(path).readlines()]

guard_chars = ["^", ">", "v", "<"]
print()
def get_guard_position(area) -> Tuple[int, int]:
    for (y_index, row) in enumerate(area):
        for (x_index, cell) in enumerate(row):
            if cell in guard_chars:
                return (y_index, x_index)

initial_y, initial_x = get_guard_position(input_area)
initial_guard_char  =input_area[initial_y][initial_x]
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

def scan_ahead(area, currY, currX, initial_direction) -> Optional[Tuple[int, int]]:
    y_direction, x_direction = rotate(initial_direction[0], initial_direction[1])
    obstacle_y = currY + initial_direction[0]
    obstacle_x = currX + initial_direction[1]
    obstacle_y_x = (obstacle_y, obstacle_x)
    if area[obstacle_y][obstacle_x] == "#":
        return None
    x = currX
    y = currY
    path = [(y,x)]
    positions = set([(y,x)])
    while True:
        next_x = x + x_direction
        next_y = y + y_direction
        if not in_area(next_y, next_x, area):
            return None
        next_field = area[next_y][next_x]
        if next_field == "#" or (next_y, next_x) == obstacle_y_x :
            y_direction, x_direction = rotate(y_direction, x_direction)
        x = x + x_direction
        y = y + y_direction
        y_x = (y, x)
        #if area[y][x] == directional_marker[(y_movement, x_movement)]:
        #    return obstacle_y_x
        if y_x in positions:
            last_index_y_x = get_last_index(path, y_x)
            possible_loop = path[last_index_y_x+1:]
            path_before_loop = path[:last_index_y_x]
            if is_sublist(possible_loop, path_before_loop):
                if test:
                    # print(path)
                    #print(f"lenpath {len(path)}, {y_x}, possible loop {possible_loop}" )
                    print(f"len path {len(path)} {last_index_y_x} {len(possible_loop)} {len(path_before_loop)}")
                    #print(f" last_index_xy {last_index_y_x} path_before_loop {path_before_loop}")
                return obstacle_y_x
        path.append(y_x)
        positions.add(y_x)
    
def get_last_index(list, elem): 
    path_reversed = list[::-1]
    first_index_path_reversed = path_reversed.index(elem)
    return len(path_reversed) - first_index_path_reversed -1 

def is_sublist(sublist, test_list) -> bool:
    res = False
    for idx in range(len(test_list) - len(sublist) + 1):
        if test_list[idx: idx + len(sublist)] == sublist:
            res = True
            break
    return res


def step_and_mark_directional(area )-> List[Tuple[int,int]]:
    possible_loop = []
    y,x = (initial_y, initial_x)
    (y_direction, x_direction) = initial_movement
    finished_steps = 0
    while True:
        possible_next_x_pos = x + x_direction
        possible_next_y_pos = y + y_direction
        if not in_area(possible_next_y_pos, possible_next_x_pos, area):
            break
        next_field = area[possible_next_y_pos][possible_next_x_pos]
        if next_field == "#":
            y_direction, x_direction = rotate(y_direction, x_direction)
        obstacle_would_loop = scan_ahead(area, y, x, (y_direction, x_direction))
        if obstacle_would_loop:
            possible_loop.append(obstacle_would_loop)
        x = x + x_direction
        y = y + y_direction
        finished_steps += 1
    return possible_loop


def print_area(area):
    result = ""
    for row in area:
        for cell in row:
            result += cell
        result += "\n"
    print(result)
# print_area()
area_puzzle_1 = [row.copy() for row in input_area]
total_steps = step_and_mark(area_puzzle_1)
# print()
# print_area(area)
def count_steps(area):
    counter = 0
    for row in area:
        for cell in row:
            if cell == "X":
                counter += 1
    return counter
print("Steps Part 1", count_steps(area_puzzle_1))

area_for_part_2 = [row.copy() for row in input_area]
possible_loops = step_and_mark_directional(area_for_part_2)
possible_loops = [pl for pl in possible_loops if pl != (initial_y, initial_x)]
set_possible_loops = set(possible_loops)

if test:
    print(possible_loops)
for pl in possible_loops:
    area_for_part_2[pl[0]][pl[1]] = "0"
if test:
    print_area(area_for_part_2)

print("Possible loops", len(possible_loops), len(set_possible_loops))


# Falsche Antworten: 1495, 1496
# Möglich: 
#   - 1569, aber da sind Duplikate mit dabei 