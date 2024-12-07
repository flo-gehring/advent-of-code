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
    direction = initial_movement
    position = (initial_y, initial_x)
    while True:
        if not in_area(position[0], position[1], area):
            break
        area[position[0]][position[1]] = "X"
        direction = calculate_next_direction(position, direction, area)
        position = add_tuple(position, direction)
        total_steps += 1
    return total_steps

directional_marker = {
     (-1, 0): "^",
        (0,1): ">",
        (1,0): "v",
        (0,-1): "<"
}

def add_tuple(t1: Tuple[int, int], t2: Tuple[int,int]) -> Tuple[int,int]:
    return (t1[0] + t2[0], t1[1] + t2[1])

def calculate_next_direction(position: Tuple[int,int], direction: Tuple[int,int], area: List[List[str]]) -> Optional[Tuple[int, int]]:
    current_direction = direction
    for _ in range(4):
        possible_next_pos = add_tuple(position, current_direction)
        if not in_area(possible_next_pos[0], possible_next_pos[1], area) or \
                area[possible_next_pos[0]][possible_next_pos[1]] != "#":
            return current_direction
        current_direction = rotate(current_direction[0], current_direction[1])
    return None


def copy_area(area):
    return [row.copy() for row in area]

def place_obstacle_in_front(area: List[List[str]], initial_position: Tuple[int,int], initial_direction: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    obstacle_y_x = add_tuple(initial_position, initial_direction)
    if not in_area(obstacle_y_x[0], obstacle_y_x[1], area):
        return None
    path = [initial_position]
    positions = set([initial_position])
    position = initial_position
    direction = initial_direction

    char_at_obstacle = area[obstacle_y_x[0]][obstacle_y_x[1]]
    area[obstacle_y_x[0]][obstacle_y_x[1]] = "#"
    while True:
        direction = calculate_next_direction(position, direction, area)
        if not direction:
            area[obstacle_y_x[0]][obstacle_y_x[1]] = char_at_obstacle
            return obstacle_y_x
        position = add_tuple(direction, position)
        if not in_area(position[0], position[1], area):
            area[obstacle_y_x[0]][obstacle_y_x[1]] = char_at_obstacle
            return None
        #if area[y][x] == directional_marker[(y_movement, x_movement)]:
        #    return obstacle_y_x
        if position in positions:
            last_index_y_x = get_last_index(path, position)
            possible_loop = path[last_index_y_x+1:]
            path_before_loop = path[:last_index_y_x]
            if is_sublist(possible_loop, path_before_loop):
                if test:
                    # print(path)
                    #print(f"lenpath {len(path)}, {y_x}, possible loop {possible_loop}" )
                    print(f"len path {len(path)} {last_index_y_x} {len(possible_loop)} {len(path_before_loop)}")
                    #print(f" last_index_xy {last_index_y_x} path_before_loop {path_before_loop}")
                area[obstacle_y_x[0]][obstacle_y_x[1]] = char_at_obstacle
                return obstacle_y_x
        path.append(position)
        positions.add(position)
    
def check_if_loops(initialPosition: Tuple[int,int], initialDirection: Tuple[int,int], area: List[List[str]]) -> bool:
    direction = initialDirection
    position = initialPosition
    size =  len(area) * len(area[0])
    steps_taken = 0
    while True:
        direction = calculate_next_direction(position, direction, area)
        if not direction:
            return True
        position = add_tuple(direction, position)
        if not in_area(position[0], position[1], area):
            return False
        if steps_taken > size + 1:
            return True
        steps_taken += 1
    
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


def find_obstacles(area)-> int:
    loops = 0
    approx_loops = len(area) * len(area[0]) 
    for y in range(len(area)): 
        for x in range(len(area[y])):
            char = area[y][x]
            if (y,x) != (initial_y, initial_x) and char != "#":
                area[y][x] = "#"
                if check_if_loops((initial_y, initial_x), initial_movement, area):
                    loops += 1
            area[y][x] = char
            print(f"Finished {y * len(area[0])  + x   } / {approx_loops} ({(y * len(area[0])  + x) / approx_loops * 100 }%)")
    return loops


def print_area(area):
    result = ""
    for row in area:
        for cell in row:
            result += cell
        result += "\n"
    print(result)
# print_area()
area_puzzle_1 = copy_area(input_area)
total_steps = step_and_mark(area_puzzle_1)
# print()
print_area(area_puzzle_1)
def count_steps(area):
    counter = 0
    for row in area:
        for cell in row:
            if cell == "X":
                counter += 1
    return counter
print("Steps Part 1", count_steps(area_puzzle_1))

area_for_part_2 = copy_area(input_area)
possible_loops = find_obstacles(area_for_part_2)


if test:
    print(possible_loops)
if test:
    print_area(area_for_part_2)

print("Possible loops", possible_loops)


# Falsche Antworten: 1495, 1496, 1614 (Mit neuer rotate methode)
# Möglich: 
#   - 1569, aber da sind Duplikate mit dabei 
#   - 1699, aber da sind Duplikate dabei