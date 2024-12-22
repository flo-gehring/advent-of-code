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
warehouse, movement  = load_input(path)
robot = find_robot(warehouse)

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
            print("False", current)
            return False 
        current = add_vec(current,  move)
    print("Moving Crate", crate_pos , current )
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


print(pretty_print(warehouse))
set_in_warehouse(robot, warehouse, ".")
print(robot)
print(pretty_print(warehouse))

for m in movement:
    robot = move(warehouse, robot, m)
    print("move", m)
    set_in_warehouse(robot, warehouse, "@")
    print(pretty_print(warehouse))
    set_in_warehouse(robot, warehouse, ".")


print(pretty_print(warehouse))