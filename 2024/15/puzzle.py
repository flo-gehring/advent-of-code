from functools import reduce

path = "2024/15/input_test_smol.txt"

def load_input(path): 
    lines = open(path).readlines()
    separating_line = lines.index("\n")
    assert separating_line > 1 and separating_line <= len(lines)
    warehouse = lines[:separating_line]
    movement = lines[separating_line+1:]
    movement_flat  =  reduce(lambda x,y: x.strip() + y.strip(), movement, "")
    return [[s for s in w.strip()] for w in warehouse], movement_flat

def find_robot(warehouse: list[list[str]]) -> tuple[int,int]:
    for (y, row) in enumerate(warehouse):
        for (x, cell) in enumerate(row):
            if cell == "@":
                return (y,x)

def set_in_warehouse(pos, warehouse: list[str], replacement):
    (y,x) = pos
    warehouse[y][x] = replacement
        

def pretty_print(input: list[list[str]]) -> str:
    result = ""
    for l in input:
        for c in l:
            result += c
        result += "\n"
    return result

def add_vec(lhs: tuple[int,int], rhs:tuple[int,int]) -> tuple[int,int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])

def scalar_mult(v: tuple[int,int], s:int) -> tuple[int,int]:
    return (int(v[0] * s), (v[1] * s))

def is_in_input(input: list[list[str]], p: tuple[int,int]) -> bool:
    len_y = len(input)
    return len_y > p[0]  and p[0] >= 0 and len(input[0]) > p[1] and len(input[0]) >= 0

def get_from(input: list[list[str]], p: tuple[int,int]) -> str:
    return input[p[0]][p[1]]

def translate_move(move: str) -> tuple[int,int]:
    return {
        "<": (0,-1),
        ">": (0,1),
        "^": (-1,0),
        "v": (1,0)
    }[move] 

def try_move_crate(warehouse: list[list[str]], crate_pos: tuple[int,int], move: str) -> bool:
    current = add_vec(crate_pos, move)
    while get_from(warehouse, current) != ".":
        if get_from(warehouse, current) == "#":
            return False 
        current = add_vec(current,  move)
    set_in_warehouse(  crate_pos,warehouse, ".")
    set_in_warehouse( current, warehouse, "O")
    return True

def move(warehouse: list[list[str]], robot: tuple[int,int], move: str) -> tuple[int,int]:
    movement_vec = translate_move(move)
    possible_next = add_vec(robot, movement_vec)
    char_at_next = get_from(warehouse, possible_next) 
    if char_at_next == "O":
        moved = try_move_crate(warehouse, possible_next, movement_vec)
        if moved:
            return possible_next
        else:
            return robot
    elif char_at_next == "#":
        return robot
    else:
        return possible_next
    
def move_puzzle2(warehouse: list[list[str]], robot: tuple[int,int], move: str) -> tuple[int,int]:
    movement_vec = translate_move(move)
    possible_next = add_vec(robot, movement_vec)
    char_at_next = get_from(warehouse, possible_next) 
    if char_at_next == "[" or char_at_next == "]":
        moved = try_move_crate_puzzle2(warehouse, possible_next, movement_vec)
        if moved:
            return possible_next
        else:
            return robot
    elif char_at_next == "#":
        return robot
    else:
        return possible_next

def move_tile_one_step(warehouse: list[list[str]], start_pos: tuple[int,int], step_dir: tuple[int,int]):
    last_tile = get_from(warehouse, start_pos)
    if last_tile == ".":
        return
    current_position = start_pos
    current_position = add_vec(current_position, step_dir)
    while True:
        current_tile = get_from(warehouse, current_position)
        set_in_warehouse(current_position, warehouse, last_tile)
        if current_tile == ".":
            break
        current_position = add_vec(current_position, step_dir)
        last_tile = current_tile

def try_move_crate_puzzle2(warehouse: list[list[str]], crate_pos: tuple[int,int], move: tuple[int,int]) -> bool:
    if move[1] != 0: # Move Horizontally  / Sideways
        print("Move horizontal")
        current = add_vec(crate_pos, move)
        while get_from(warehouse, current) != ".":
            if get_from(warehouse, current) == "#":
                return False 
            current = add_vec(current,  move)
        move_tile_one_step(warehouse, crate_pos, move)
        return True
    else: # Move Vertically
        print("Move vertical")
        movable_crates = get_movable_crates(warehouse, crate_pos, move)
        if movable_crates:
            for crate in movable_crates:
                move_tile_one_step(warehouse, crate[0], move)
                move_tile_one_step(warehouse, crate[1], move)
            return True
        else:
            return False
            

def get_movable_crates(
        warehouse,
          crate_pos: tuple[int,int],
            dir: tuple[int,int]
            ) -> list[tuple[tuple[int,int], tuple[int,int]]]:
    crate_symbol_at_create_pos = get_from(warehouse, crate_pos)
    crate_pos_2 = None
    crate_pos_is_left = None
    if crate_symbol_at_create_pos == "]":
        crate_pos_is_left = False
        crate_pos_2 = add_vec(crate_pos, (0,-1))
    else: 
        crate_pos_2 = add_vec(crate_pos, (0,1))
        crate_pos_is_left = True
    crate = (crate_pos, crate_pos_2) if crate_pos_is_left else (crate_pos_2, crate_pos)
    crates = [crate]
    next_1 = add_vec(crate_pos, dir)
    next_2 = add_vec(crate_pos_2, dir)
    next_char_1 =get_from(warehouse, next_1)
    next_char_2 =  get_from(warehouse, next_2) 
    crate_symbols = ["[", "]"]
    if next_char_1 == "." and next_char_2 == ".":
        return crates
    elif next_char_2 == "#" or next_char_2 == "#":
        return []
    elif next_char_2 in crate_symbols  and next_char_1 in crate_symbols:
        movable_crates_from1 = get_movable_crates(warehouse, next_1, dir)
        movable_crates_from2 = get_movable_crates(warehouse, next_2, dir)
        if not movable_crates_from1 or movable_crates_from2:
            return []
        crates.extend(movable_crates_from2)
        crates.extend(movable_crates_from1)
        return crates
    elif next_char_1 in crate_symbols:
        movable_crates_from1 = get_movable_crates(warehouse, next_1, dir)
        if not movable_crates_from1:
            return []
        crates.extend(movable_crates_from1)
        return crates
    elif next_char_2 in crate_symbols:
        movable_crates_from2 = get_movable_crates(warehouse, next_2, dir)
        if not movable_crates_from2:
            return []
        crates.extend(movable_crates_from2)
        return crates
    raise Exception(f"Unreachable state {next_char_1}, {next_char_2}")

                                                                          

   

def calculate_solution_puzzle1(warehouse: list[list[str]]) -> int:
    result = 0
    for (y, row) in enumerate(warehouse):
        for (x, char) in enumerate(row):
            if char == "O":
                result += 100 * y + x
    return result

def find_robot(warehouse: list[list[str]]) -> tuple[int,int]:
    for (y, row) in enumerate(warehouse):
        for (x, cell) in enumerate(row):
            if cell == "@":
                return (y,x)

def move_robot(warehouse: list[list[str]], movements: list[str]) -> None:
    robot = find_robot(warehouse)
    set_in_warehouse(robot, warehouse, ".")
    for m in movements:
        robot = move(warehouse, robot, m)

def move_robot_puzzle2(warehouse: list[list[str]], movements: list[str]):
    robot = find_robot(warehouse)
    set_in_warehouse(robot, warehouse, ".")
    for m in movements:
        robot = move_puzzle2(warehouse, robot, m)
        set_in_warehouse(robot, warehouse, "@")
        print("Movement", m )
        print(pretty_print(warehouse))
        set_in_warehouse(robot, warehouse, ".")


def puzzle1(warehouse: list[list[str]], movements: list[str]) -> tuple[int,int]:
    move_robot(warehouse, movements)
    return calculate_solution_puzzle1(warehouse)

warehouse, movement  = load_input(path)

def copy_input(input: list[list[str]]) -> list[list[str]]:
    result = []
    for i in input:
        result.append(i.copy())
    return result


def expand_warehouse(warehouse: list[list[str]]) -> list[list[str]]:
    result = []
    for row in warehouse:
        new_row = []
        for string in row:
            if string == "#":
                new_row.append("#")
                new_row.append("#")
            elif string == "O":
                new_row.append("[")
                new_row.append("]")
            elif string == ".":
                new_row.append(".")
                new_row.append(".")
            elif string == "@":
                new_row.append("@")
                new_row.append(".")
            else:
                raise Exception(f"Unknown Tile {string}" )
        result.append(new_row)
    return result

def puzzle2(warehouse: list[list[str]], movements: list[str])-> int:
    expanded = expand_warehouse(warehouse)
    print(pretty_print(expanded))
    move_robot_puzzle2(expanded, movements)
    print(pretty_print(expanded))

print("Solution Puzzle 1", puzzle1(copy_input(warehouse), movement))
print("Solution Puzzle 2", puzzle2(copy_input(warehouse), movement))
