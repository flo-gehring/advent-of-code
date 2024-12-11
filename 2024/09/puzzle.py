input = open("2024/09/input.txt").read()

def is_file(index: int) -> bool:
    return index % 2 == 0

def file_id(index: int) -> int:
    assert is_file(index)
    return int(index / 2)


def checksum_calc(index_on_disk: int, file_id: int, num_blocks: int) -> int: 
    checksum_list =  [(block_on_file , int(file_id)) for block_on_file in 
                    range(index_on_disk, index_on_disk + num_blocks ) ]
    return sum([x *y for (x,y) in checksum_list])
    

def part1(input):
    """Calculate the checksum.
    i will iterate through the disk representation and fill up everything as i go
    """
    input = [int(char) for char in input]
    checksum =0
    index_on_disk = 0
    index_of_rightmost_file = len(input) -1
    for (index_input_string, symbol) in enumerate(input):
        block_count = symbol
        if is_file(index_input_string) and file_id(index_input_string) > file_id(index_of_rightmost_file):
            break
        if is_file(index_input_string):
            checksum += checksum_calc(index_on_disk, file_id(index_input_string), block_count)
            input[index_input_string] = 0
            index_on_disk += block_count
        else: 
            free_blocks = block_count
            while free_blocks > 0: 
                remaining_blocks_of_rightmost_file = input[index_of_rightmost_file]
                if remaining_blocks_of_rightmost_file <= free_blocks:
                    checksum += checksum_calc(index_on_disk, file_id(index_of_rightmost_file), remaining_blocks_of_rightmost_file)
                    index_on_disk += remaining_blocks_of_rightmost_file
                    free_blocks -= remaining_blocks_of_rightmost_file
                    input[index_of_rightmost_file] = 0
                    index_of_rightmost_file -= 2
                else:
                    checksum += checksum_calc(
                        index_on_disk, file_id(index_of_rightmost_file), free_blocks
                    )
                    index_on_disk += free_blocks
                    input[index_of_rightmost_file] -= free_blocks
                    free_blocks = 0 # implicit break
                if index_of_rightmost_file <= index_input_string:
                    break
    return checksum


def calculate_checksum_part2(drive_layout):
    index_on_disk = 0
    checksum = 0
    for (file, block_count) in drive_layout:
        if file != -1:
            checksum += checksum_calc(index_on_disk, file, block_count)
        index_on_disk += block_count
    return checksum

def part2(input):
    input = [int(char) for char in input]
    index_on_disk = 0
    drive_layout = [    ]
    for (index_input_string, blocks_of_file) in enumerate(input):
        if is_file(index_input_string):
            drive_layout.append( (file_id(index_input_string), blocks_of_file))
            index_on_disk += blocks_of_file
        else: 
            drive_layout.append((-1, blocks_of_file))
    for file in list(range( int(len(input) /2 +1)))[::-1]:
            layout_def = [x for x in drive_layout if x[0] == file][0]
            index = drive_layout.index(layout_def)
            drive_layout.pop(index)
            blocks_of_file = layout_def[1]
            for (idx, (f_id, freeblocks)) in enumerate(drive_layout[:index]):
                if freeblocks >= blocks_of_file and f_id == -1:
                    insert = [layout_def]
                    if blocks_of_file < freeblocks:
                        insert.append( (-1,   freeblocks -blocks_of_file))
                    new_drive_layout = []
                    drive_layout.insert(index, (-1, blocks_of_file))
                    drive_layout_split_left  = drive_layout[:idx].copy()
                    drive_layout_split_right = drive_layout[idx+1:]
                    new_drive_layout.extend(drive_layout_split_left)
                    new_drive_layout.extend(insert)
                    new_drive_layout.extend(drive_layout_split_right)
                    drive_layout = new_drive_layout
                    break
            else:
                drive_layout.insert(index, layout_def )
    return  calculate_checksum_part2(drive_layout)
    

print("Solution Part 1", part1(input))
# Wrong: 6485877793755 (too high)
# Correct: 6344673854800

# Wrong:        8515929533392 (too high)
#               9997826754152
# Wrong :       6356335200500 (too low)
# Correct:      6360363199987
print("Solution Part 2", part2(input))
