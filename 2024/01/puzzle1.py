from functools import reduce
f = open("2024/01/input_1.txt")#

tuples = [(int(line.split()[0]), int(line.split()[1])) for line in f.readlines()]
tuples_and_pos = [(tuples[x], x) for x in range(len(tuples))]
list_1_and_pos = [(tp[0][0], tp[1] ) for tp in tuples_and_pos ]
list_2_and_pos = [(tp[0][1], tp[1] ) for tp in tuples_and_pos ]
print("Number and pos")
print(list_1_and_pos[1])
list_1_and_pos = sorted(list_1_and_pos, key=lambda x : x[0])
list_2_and_pos = sorted(list_2_and_pos, key=lambda x : x[0])
matching_numbers = list(zip(list_1_and_pos, list_2_and_pos))
print("Matching numbers ")
print(matching_numbers[0])
distances = [abs(a[0][0] -a[1][0]) for a in matching_numbers]
print(distances[1])
total_distance = reduce(lambda a,b:  a + b, distances)
print("Total distance")
print(total_distance)

list1 = [t[0] for t in tuples]
list2 = [t[1] for t in tuples]

def count_occurence(x, l):
    return sum(
        [1 for y in l if x == y]
    )

counts_of_1 = [
    count_occurence(x, list2) * x for x in list1
]

similiarity = reduce(lambda a,b:  a + b, counts_of_1)
print(similiarity)