from typing import Optional
from sortedcontainers import SortedDict, SortedListWithKey
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

def part2(input):
    input = [int(char) for char in input]
    # Build initial Disk Layout, save file ids and the block range in a sorted container (sorted dict) where the block numbers are 
    # also stored
    
    index_on_disk = 0
    drive_layout = SortedDict()
    free_space = SortedListWithKey(key= lambda t:  t[1])
    for (index_input_string, block_count) in enumerate(input):
        if is_file(index_input_string):
            drive_layout[file_id(index_input_string)] = (index_on_disk, block_count)
            index_on_disk += block_count
        else: 
            # Create a sorted container, where free blocks can be found by their size
            # The Dictionary contains tuples with the content (index_on_disk, free_space)
            free_space.add((index_on_disk, block_count))
            index_on_disk += block_count
    input_len = len(input)
    print(input_len)
    for reverse_skip_index_dont_ask, block_count in enumerate(input[::-2]):
        would_be_index = (input_len-1) - 2 * reverse_skip_index_dont_ask
        # Try to move File to the left
        index_in_free_space = find_index_in_free_space(block_count, free_space)
        if index_in_free_space == len(free_space):
            print("Not enough space" , file_id(would_be_index))
            continue 
        else:
            (index_on_disk_free_space, free_blocks) = free_space.pop(index_in_free_space)
            print("Move it!", file_id(would_be_index), index_in_free_space)
            drive_layout[file_id(would_be_index)] = (index_on_disk_free_space, block_count)

            free_space.add((index_in_free_space + block_count, free_blocks - block_count))
    
    return  drive_layout, sum([checksum_calc(iod, file, n_blocks) for (file, (iod, n_blocks)) in drive_layout.items()])


def find_index_in_free_space(block_count: int, free_space: SortedListWithKey) -> int:
    index_left = free_space.bisect_key_left(block_count)
    index_right = free_space.bisect_key_left(block_count +1)
    if index_left < len(free_space):
        if index_left == index_right:
            return index_left
        slice = free_space[index_left:index_right]
        slice_sorted = sorted(slice, key=lambda x: x[0])
        entry = slice_sorted[0]
        return free_space.index(entry)
    return len(free_space)
    



print("Solution Part 1", part1(input))
# Wrong: 6485877793755 (too high)
# Correct: 6344673854800

print(part2(input))