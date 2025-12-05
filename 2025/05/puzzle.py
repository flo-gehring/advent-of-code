f  = open("advent-of-code-input/2025/05/input.txt" )

ranges = []
ingredients = []
in_range = True
for line  in f.readlines():
    if len(line.strip()) == 0:
        in_range = False
        continue
    if in_range:
        
        ranges.append((int(line.strip().split("-")[0]), (int(line.strip().split("-")[1]))))
    else: 
        ingredients.append(int(line.strip()))

fresh_ingredients = []


def point_in_range(p: int, range:tuple[int,int]) :
    return p >= range[0] and p <= range[1]

def in_range(ingredient):
    for (start, end) in ranges:
        if ingredient >= start and ingredient <= end:
            return True
    return False



for ingredient in ingredients:
    if in_range(ingredient):
        fresh_ingredients.append(ingredient)


sorted_ranges = sorted(ranges, key=lambda x: x[0])
print(sorted_ranges)
overlap_free = False
new_ranges = []

def overlaps(first: tuple[int,int], second: tuple[int,int]):
    """
    Docstring for overlaps
    
    :param first: Description
    :type first: tuple[int, int]
    :param second: Description
    :type second: tuple[int, int]
    """
    return (point_in_range(first[1], second ) or point_in_range(first[0], second)) or \
        (point_in_range(second[0], first) or point_in_range(second[1], first))


def unify_ranges(range1, range2):
    return (min(range1[0], range2[0]), max(range1[1], range2[1]))

while not overlap_free:
    overlap_free = True
    for i in range(0, len(sorted_ranges) -1):
        if overlaps(sorted_ranges[i], sorted_ranges[i+1]):
            overlap_free = False
            new_ranges.append(unify_ranges(sorted_ranges[i], sorted_ranges[i+1]))
            new_ranges += sorted_ranges[i+2:]
            break
        else:
            new_ranges.append(sorted_ranges[i])
    else:
        new_ranges.append(sorted_ranges[-1])
    sorted_ranges = new_ranges
    new_ranges = []

# 354279340445696 too high
print(sorted_ranges)

any_overlaps = False
for i in range(0, len(sorted_ranges) -1):
    any_overlaps = any_overlaps or overlaps(sorted_ranges[i], sorted_ranges[i+1])
print(any_overlaps)
print(sum([(end-start) +1 for (start, end) in sorted_ranges]))