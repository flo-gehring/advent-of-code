from itertools import combinations
input : list[str]= [l.strip() for l in open("2024/08/input.txt").readlines()]
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

def calculate_antinodes(antenna_locations: list[tuple[int,int]]) -> list[tuple[int,int]]:
    antenna_combinations = combinations(antenna_locations, r=2)
    result = []

    for (antenna1, antenna2) in antenna_combinations:
        print(antenna1, antenna2)
        result += calculate_antinodes_for_antennas_part1(antenna1, antenna2)
    return result

def add_vector(lhs: tuple[int,int], rhs: tuple[int,int]) -> tuple[int,int]: 
    return (lhs[0]+rhs[0], lhs[1 ]+  rhs[1])

def scalar_mult(v: tuple[int,int], s: int) -> tuple[int,int]:
    return (v[0] * s, v[1] * s)

def calculate_antinodes_for_antennas_part1(antenna1: tuple[int, int], antenna2: tuple[int,int])->list[tuple[int,int]]:
    vec_a1_a2 = add_vector(antenna2, scalar_mult(antenna1, -1))
    vec_a2_a1 = scalar_mult(vec_a1_a2, -1)
    return [add_vector(antenna2, vec_a1_a2), add_vector(antenna1, vec_a2_a1)] 

def part_1(grid: list[str]):
    antinode_locations = set()
    antenna_types = get_antenna_types(grid)
    grid_y_size, grid_x_size = (len(grid), len(grid[0]))
    print("Antenna types", antenna_types)
    for antenna_type in antenna_types:
        antinode_locations_antenna = [
            (y, x) for (y,x) in 
            calculate_antinodes(get_antenna_locations(antenna_type, grid))
            if y < grid_y_size and y >= 0 and x < grid_x_size and x >= 0
        ]
        antinode_locations = antinode_locations.union(antinode_locations_antenna)
    return antinode_locations

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
print(locations)
marked_locations = mark_locations_on_grid(input, locations, "#")
print(pretty_grid(marked_locations))
print("Solution Part 1: ", len(locations))
