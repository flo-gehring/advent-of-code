input = open("2024/09/input_test.txt").read()

print(len(input))
def is_file(index: int) -> bool:
    return index % 2 == 0
def file_id(index: int) -> int:
    assert is_file(index)
    return int(index / 2)


def checksum_calc(index_on_disk: int, file_id: int, num_blocks: int) -> int: 
    checksum_list =  [(block_on_file , int(file_id)) for block_on_file in 
                    range(index_on_disk, index_on_disk + num_blocks )
                ]
    print(checksum_list)
    return sum([x *y for (x,y) in checksum_list])

    

def part1(input):
    """Calculate the checksum.
    i will iterate through the disk representation and fill up everything as i go
    """
    input = [int(char) for char in input]
    checksum =0
    index_on_disk = 0
    index_of_rightmost_file = len(input) -1
    remaining_blocks_of_rightmost_file = input[index_of_rightmost_file]
    for (index_input_string, symbol) in enumerate(input):
        block_count = symbol
        if is_file(index_input_string) and file_id(index_input_string) > file_id(index_of_rightmost_file):
            print("break, file id reached")
            break
        if is_file(index_input_string):
            print("File", " idx input", index_input_string, "file id", file_id(index_input_string))
            checksum += checksum_calc(index_on_disk, file_id(index_input_string), block_count)
            input[index_input_string] = 0
            index_on_disk += block_count
        else: 
            free_blocks = block_count
            print("Free Space", block_count)
            while free_blocks > 0: 
                if remaining_blocks_of_rightmost_file <= free_blocks:
                    print("All Free Blocks")
                    checksum += checksum_calc(index_on_disk, file_id(index_of_rightmost_file), remaining_blocks_of_rightmost_file)
                    index_on_disk += remaining_blocks_of_rightmost_file
                    free_blocks -= remaining_blocks_of_rightmost_file
                    input[index_of_rightmost_file] = 0
                    index_of_rightmost_file -= 2
                    remaining_blocks_of_rightmost_file = input[index_of_rightmost_file]
                else:
                    print("Fill Without remaining")
                    checksum += checksum_calc(
                        index_on_disk, file_id(index_of_rightmost_file), free_blocks
                    )
                    index_on_disk += free_blocks
                    remaining_blocks_of_rightmost_file -= free_blocks
                    input[index_of_rightmost_file] -= free_blocks
                    free_blocks = 0 # implicit break

    return checksum


print("Solution Part 1", part1(input))