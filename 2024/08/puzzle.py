from itertools import combinations

input : list[str]= [l.strip() for l in open("2024/08/input.txt").readlines()]

def part_1(grid: list[str]):
    antinode_locations = set()
    antenna_types = get_antenna_types(grid)
    grid_y_size, grid_x_size = (len(grid), len(grid[0]))
    for antenna_type in antenna_types:
        antinode_locations_antenna = [
            (y, x) for (y,x) in 
            calculate_antinodes_puzzle_part_1(get_antenna_locations(antenna_type, grid))
            if y < grid_y_size and y >= 0 and x < grid_x_size and x >= 0
        ]
        antinode_locations = antinode_locations.union(antinode_locations_antenna)
    return antinode_locations

def part_2(grid: list[str]):
    antinode_locations = set()
    antenna_types = get_antenna_types(grid)
    grid_size = (len(grid), len(grid[0]))
    for antenna_type in antenna_types:
        antinode_locations_antenna = calculate_antinodes_puzzle_part_2(
            get_antenna_locations(antenna_type, grid),
            grid_size
            )
        antinode_locations = antinode_locations.union(antinode_locations_antenna)
    return antinode_locations

def get_antenna_types(grid: list[str]) -> set[str]:
    result = set()
    for row in grid:
        result = result.union([char for char in row if char != "."])
    return result

def get_antenna_locations(antenna_type: str, grid: list[str]) -> list[tuple[int,int]]:
    result = []
    for (y, row) in enumerate(grid):
        for (x, cell) in enumerate(row):
            if cell == antenna_type:
                result.append((y,x))
    return result

def calculate_antinodes_puzzle_part_1(antenna_locations: list[tuple[int,int]]) -> list[tuple[int,int]]:
    """Calculates the antinode locations of a certain puzzle antenna type for part 1 of the puzzle. 
        Returns a list that could possibly contain the same location twice and be out of bounds of the grid
    """
    antenna_combinations = combinations(antenna_locations, r=2)
    result = []
    for (antenna1, antenna2) in antenna_combinations:
        result += calculate_antinodes_for_antennas_part1(antenna1, antenna2)
    return result

def calculate_antinodes_puzzle_part_2(antenna_locations: list[tuple[int,int]], grid_size: tuple[int,int]) -> set[tuple[int,int]]:
    """Calculates the antinode locations of a certain puzzle antenna type for part 2 of the puzzle. 
        Returns a set (no duplicate antinode location) and is guranteed to be in bounds of the grid
    """
    antenna_combinations = combinations(antenna_locations, r=2)
    result = set()
    for (antenna1, antenna2) in antenna_combinations:
        result  = result.union( calculate_antinodes_for_antennas_part2(antenna1, antenna2, grid_size))
    return result

def calculate_antinodes_for_antennas_part2(antenna1: tuple[int, int], antenna2: tuple[int,int], grid_size: tuple[int,int]) -> set[tuple[int,int]]:
    """Simply draws a line on the grid that connects the two antennas with the smallest possible step size.
    """
    vec_a1_a2 = add_vector(antenna2, scalar_mult(antenna1, -1))
    vec_a1_a2_reduced = reduce_vector_discrete(vec_a1_a2)
    return create_line(antenna1, vec_a1_a2_reduced, grid_size)

def create_line(pos: tuple[int,int], step:tuple[int,int], bounds: tuple[int,int]) -> set[tuple[int, int]]:
    """Draws a line in a discrete grid with bounds, starting from pos with stepsize step
    """
    current_pos = pos
    result = set()
    while in_bounds(current_pos, bounds):
        result.add(current_pos)
        current_pos = add_vector(current_pos, step)
    negative_step = scalar_mult(step, -1)
    current_pos = pos
    while in_bounds(current_pos, bounds):
        result.add(current_pos)
        current_pos = add_vector(current_pos, negative_step)
    return result

def in_bounds(pos: tuple[int,int], bounds: tuple[int,int]) -> bool:
    return pos[0] >= 0 and pos[0] < bounds[0] and pos[1] >= 0 and pos[1] < bounds[1]

def reduce_vector_discrete(v: tuple[int,int]) -> tuple[int,int]:
    """ Create a vector that represents the smallest possible step of the same angle as the inputvector.
    The idea is, that for this puzzle we want to move in a line between two nodes along a grid.
    What does this mean? 
        -> For a (2,2) Vector for example, the  step is (1,1)
        -> For a (4,0) Vector, the step is (1,0)
        -> For a (6,3) Vector, the step is (2,1)
        -> What About a (5,4) Vector ? -> Dont do anything
    """
    v_0 = v[0]
    v_1 = v[1]
    lt_eq = min(v_0, v_1)
    g = max(v_0, v_1)
    if lt_eq == 0:
        # If both are zero the calling method has messed up. This is not the place to check but i dont want to get stuck in a loop
        assert v_1 == 0 ^ v_0 == 0 
        return (1,0) if v_1 == 0 else (0,1)
    elif g % lt_eq == 0:
        return (int(v_0 / lt_eq), int(v_1 / lt_eq))
    else:
        return v

def add_vector(lhs: tuple[int,int], rhs: tuple[int,int]) -> tuple[int,int]: 
    return (lhs[0]+rhs[0], lhs[1 ]+  rhs[1])

def scalar_mult(v: tuple[int,int], s: int) -> tuple[int,int]:
    return (v[0] * s, v[1] * s)

def calculate_antinodes_for_antennas_part1(antenna1: tuple[int, int], antenna2: tuple[int,int])->list[tuple[int,int]]:
    vec_a1_a2 = add_vector(antenna2, scalar_mult(antenna1, -1))
    vec_a2_a1 = scalar_mult(vec_a1_a2, -1)
    return [add_vector(antenna2, vec_a1_a2), add_vector(antenna1, vec_a2_a1)] 

def mark_locations_on_grid(grid: list[str], locations: list[tuple[int,int]], marker: str) -> list[str]:
    grid_copy = [list(row) for row in grid]
    for (y,x) in locations:
        grid_copy[y][x] = marker
    return ["".join(row) for row in grid_copy]

def pretty_grid(grid: list[str]) -> str:
    result = ""
    for row in grid:
        result += row + "\n"
    return result

locations = part_1(input)
marked_locations = mark_locations_on_grid(input, locations, "#")
print("Grid Part 1")
print(pretty_grid(marked_locations))
print("Solution Part 1: ", len(locations))

print()
locations_part2 = part_2(input)
print("Grid Part 2")
marked_location_part2 = mark_locations_on_grid(input, locations_part2, "*")
print(pretty_grid(marked_location_part2))
print("Solution Part2", len(locations_part2))