base_path = "advent-of-code-input/2025/07/" 
test_input = False
path = base_path + ("test.txt" if test_input else "input.txt")
f  = open( path)
grid = [l.strip() for l in f.readlines()]

def move_line(to_line:int, prev_beam_indices:list[int], grid:list[str])->tuple[int, list[int]]:
    new_beam_indices = []
    splitters_hit = 0
    for beam_index in prev_beam_indices:
        if grid[to_line][beam_index] == "^":
            splitters_hit += 1
            left = beam_index -1
            right = beam_index +1
            if left > 0: 
                new_beam_indices.append(left)
                assert grid[to_line][left] != "^"
            if right < len(grid[to_line]):
                new_beam_indices.append(right)
                assert grid[to_line][right] != "^"
        else:
            new_beam_indices.append(beam_index)
    return (splitters_hit, list(set(new_beam_indices)))

beam_indices =  [grid[0].index("S")]
total_splitters_hit = 0
for i in range(1, len(grid)):
    splitters_hit, beam_indices  = move_line(i, beam_indices, grid)
    total_splitters_hit += splitters_hit


print("Part 1", total_splitters_hit)

def move_timelines(to_line:int, timelines:list[list[int]], grid:list[str])->list[list[int]]:
    timelines_out_of_bounds = 0
    time_line = [0 for _ in list(grid[to_line]) ]
    previous_step_timeline = timelines[-1]
    for  idx in range(len(previous_step_timeline)):
        if grid[to_line][idx] == "^":
            left = idx -1
            right = idx +1
            if left >= 0: 
                assert grid[to_line][left] != "^"
                time_line[left] = time_line[left] +  previous_step_timeline[idx]
            if left < 0:
                timelines_out_of_bounds +=  +  previous_step_timeline[idx]
            if right < len(grid[to_line]):
                assert grid[to_line][right] != "^"
                time_line[right] = time_line[right] + previous_step_timeline[idx]
            if right >= len(grid[to_line]):
                timelines_out_of_bounds +=  +  previous_step_timeline[idx]
        else:
            time_line[idx] += previous_step_timeline[idx]
    return (timelines_out_of_bounds, time_line)

initial_timeline =  [0 if x != "S" else 1 for x in (grid[0].strip())]
timeline = [initial_timeline]
last_timeline = initial_timeline
out_of_bound_timelines = 0
for i in range(1, len(grid)):

    (out_of_bounds, last_timeline)  = move_timelines(i, timeline,  grid)
    out_of_bound_timelines += out_of_bounds
    timeline.append(last_timeline)

def print_timeline(tl):
    for t in tl:
        print ("\t".join([str(i) for i in t]))

# print_timeline(timeline)
print("Part 2", sum(last_timeline) + out_of_bound_timelines)



