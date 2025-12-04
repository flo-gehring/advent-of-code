f  = open("advent-of-code-input/2025/04/input.txt" )
grid = [[cell for cell in line.strip()] for line in f.readlines()]


accessible_rolls = 0
for (y, row) in enumerate(grid):
    for (x, cell) in enumerate(row):
        neighboring_rolls = 0
        if cell != "@":
            continue
        for y_offset in  range(-1,2):
            for x_offset in range(-1,2):
                if y_offset == 0 and x_offset == 0:
                    continue
                y_to_check = y + y_offset
                x_to_check = x + x_offset
                out_of_bounds =y_to_check < 0 or y_to_check >= len(grid) or x_to_check < 0 or x_to_check >= len(row)
                if out_of_bounds:
                      continue
                if grid[y_to_check][x_to_check] == "@":
                    neighboring_rolls += 1
        if neighboring_rolls < 4:
            accessible_rolls += 1
print(accessible_rolls)
                
