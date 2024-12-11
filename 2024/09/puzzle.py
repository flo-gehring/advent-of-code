from typing import Optional
from sortedcontainers import SortedDict, SortedList
input = open("2024/09/input_test.txt").read()

print(len(input))
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

def pretty_print_drive(drive_layout: SortedDict):
    print(drive_layout)
    sorted_by_disk = SortedList(drive_layout.items(), key=lambda x: x[1][0]) 
    s = ""
    for i in range(len(sorted_by_disk) -1):
        current_file, next_file =sorted_by_disk[i], sorted_by_disk[i+1]
        current_index = current_file[1][0]
        file = current_file[0]
        next_index = next_file[1][0]
        current_block_count = current_file[1][1]
        s += str(file) * current_block_count + "." * (next_index - (current_index + current_block_count))
    last_file = sorted_by_disk[-1]
    s += str(last_file[0]) * last_file[1][1]
    return s

def part2(input):
    input = [int(char) for char in input]
    # Build initial Disk Layout, save file ids and the block range in a sorted container (sorted dict) where the block numbers are 
    # also stored
    
    index_on_disk = 0
    drive_layout = SortedDict()
    # Create a dictionary, where for each free block count a list of available indices can be looked up
    free_space = dict([(free_blocks, SortedList()) for free_blocks in range(10)])
    for (index_input_string, block_count) in enumerate(input):
        if is_file(index_input_string):
            drive_layout[file_id(index_input_string)] = (index_on_disk, block_count)
            index_on_disk += block_count
        else: 
            free_space[block_count].add(index_on_disk)
            index_on_disk += block_count
    input_len = len(input)
    for reverse_skip_index_dont_ask, block_count in enumerate(input[::-2]):
        index_on_disk = (input_len-1) - 2 * reverse_skip_index_dont_ask
        # Try to move File to the left
        location = find_index_in_free_space(block_count, free_space)
        if location is None:
            continue
        (free_space_dict_key, disk_index_start_free_space)  = location
        drive_layout[file_id(index_on_disk)] = (disk_index_start_free_space, block_count)
        free_space[free_space_dict_key].remove(disk_index_start_free_space)
        free_space[free_space_dict_key - block_count].add(disk_index_start_free_space + block_count)
    return  drive_layout, sum([checksum_calc(iod, file, n_blocks) for (file, (iod, n_blocks)) in drive_layout.items()])


def find_index_in_free_space(block_count: int, free_space: dict[int, SortedList]) -> Optional[tuple[int, int]]:
    """Returns the block_count of the dict and the index on disk. None if nothing fits
    """
    leftmost_spot_per_free_block_count = [
        (free_blocks, free_space[free_blocks][0]) for free_blocks in range(block_count, 10)
        if len(free_space[free_blocks]) != 0
    ]
    if len(leftmost_spot_per_free_block_count) == 0:
        return None
    return sorted(leftmost_spot_per_free_block_count, key=lambda x: x[1])[0]
    



print("Solution Part 1", part1(input))
# Wrong: 6485877793755 (too high)
# Correct: 6344673854800
drive_layout, checksum = part2(input)
# Wrong: 8515929533392 (too high)
#        9997826754152
print(pretty_print_drive(drive_layout))
print(checksum)