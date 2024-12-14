file = "2024/11/input.txt"

input = [int(s) for s in open(file).read().split()]


def blink(input: list[int]) -> list[int]:
    new_line = []
    for  stone in input:
        if stone == 0:
            new_line.append(1)
        elif len(str(stone)) % 2 == 0:
            str_stone = str(stone)
            half = int(len(str_stone) / 2)
            first_stone = int(str_stone[:half])
            second_stone = int(str_stone[half:])
            new_line.append(first_stone)
            new_line.append(second_stone)
        else:
            new_line.append(stone * 2024)
    return new_line

def part1(input: list[int], num_blinks:int) -> list[int]:
    for _ in range(num_blinks):
        input = blink(input)
    return input 


def blink_stone(stone: int, num_blinks: int) -> int:
    str_stone = str(stone)
    half = int(len(str_stone) / 2)
    if num_blinks == 0:
        return 1
    if stone == 0:
        return blink_stone(1, num_blinks -1)
    elif len(str_stone) % 2 == 0:
        first_stone = int(str_stone[:half])
        second_stone = int(str_stone[half:])
        return blink_stone(first_stone, num_blinks-1) + blink_stone(second_stone, num_blinks-1)   
    else:
        return blink_stone(stone * 2024, num_blinks-1)

def blink_stone_lookup(stone, lookup_table: dict[int, dict[int, int]], num_blinks=75)->int:
    if num_blinks == 0:
        return 1
    if stone in lookup_table:
        if num_blinks in lookup_table[stone]:
            print("Hit!")
            return lookup_table[stone][num_blinks]
    else:
        lookup_table[stone] = dict()

    str_stone = str(stone)
    len_str = len(str_stone) 
    result = None
    if stone == 0:
        result = blink_stone_lookup(1, lookup_table, num_blinks -1)
        
    elif len_str % 2 == 0:
        half = int(len_str/ 2)
        first_stone = int(str_stone[:half])
        second_stone = int(str_stone[half:])
        stone_lhs = blink_stone_lookup(first_stone,lookup_table,  num_blinks-1)
        stone_rhs = blink_stone_lookup(second_stone, lookup_table, num_blinks-1)
        result = stone_lhs + stone_rhs
    else:
        result  = blink_stone_lookup(stone * 2024,lookup_table, num_blinks-1)
    lookup_table[stone][num_blinks] = result
    return result

def blink_stones_lookup(input, num_blinks=75):
    lookup_table = dict()
    result = 0
    for stone in sorted(input):
        result += blink_stone_lookup(stone, lookup_table, num_blinks=num_blinks)
        print("Blinked ", stone)
    return result

def part2(input, num_blinks=75):
    result = 0
    for stone in input:
        result += blink_stone(stone, num_blinks)
    return result

stones = part1(input, 25)
print("Solution Part 1", len(stones))
print("Soltution Part 2 lookup", blink_stones_lookup(input, num_blinks=75))
print("Solution Part 2", part2(input, num_blinks=25))
    