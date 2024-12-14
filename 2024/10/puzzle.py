input_path = "2024/10/input.txt"
input = [[int(c) for c in line.strip() ] for line in open(input_path).readlines()]

def walk_trail(y: int, x:int, input: list[list[int]]) -> list[tuple[int,int]]:
    if input[y][x] == 9:
        return [(y,x)]
    reachable_nines = []
    for (y_dir, x_dir) in [(-1,0), (1,0), (0,-1), (0,1)]:
        next_y = y + y_dir
        next_x = x+x_dir
        if next_x >= len(input) or next_y >= len(input[next_x]) or next_x < 0 or next_y < 0:
            continue
        if input[next_y][next_x] - input[y][x] == 1:
            reachable_nines.extend(walk_trail(next_y, next_x, input))
    return set(reachable_nines)

def part1(input):
    score = 0
    for (y, row) in enumerate(input):
        for (x, num) in enumerate(row):
            if num == 0:
                reachable_nines = walk_trail(y,x,input)
                score += len(set(reachable_nines))
    return score

def find_num_paths(y: int, x:int, input: list[list[int]]) -> int:
    unique_paths = 0
    if input[y][x] == 9:
        return 1
    for (y_dir, x_dir) in [(-1,0), (1,0), (0,-1), (0,1)]:
        next_y = y + y_dir
        next_x = x+x_dir
        if next_x >= len(input) or next_y >= len(input[next_x]) or next_x < 0 or next_y < 0:
            continue
        if input[next_y][next_x] - input[y][x] == 1:
            unique_paths += find_num_paths(next_y, next_x, input)            
    return unique_paths

def part2(input):
    score = 0
    for (y, row) in enumerate(input):
        for (x, num) in enumerate(row):
            if num == 0:
                num_paths = find_num_paths(y,x,input)
                score += num_paths
    return score


print("Solution Part 1", part1(input))
print("Solution Part 2", part2(input))