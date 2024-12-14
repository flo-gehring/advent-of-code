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

stones = part1(input, 25)
print("Solution Part 1", len(stones))