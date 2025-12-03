f  = open("advent-of-code-input/2025/03/input.txt" )

banks = [
    [int(battery) for battery in bank.strip()] for bank in f.readlines()
]

print(banks)
jolts = []
for bank in banks:
    first_battery =  max(bank[:-1])
    index_of_first = bank.index(first_battery)
    second_battery = max(bank[index_of_first+1:])
    jolts.append(int(str(first_battery) + str(second_battery)))
print(jolts)
print(sum(jolts))

jolts = []
for bank in banks:
    first_index_search_space = 0
    jolt = ""
    for i in range(12):
        searchable  = bank[first_index_search_space:len(bank)-(11-i)]
        battery = max(searchable)
        jolt += str(battery)
        first_index_search_space = bank.index(battery, first_index_search_space) + 1
    jolts.append(int(jolt))

print(jolts)
print(sum(jolts))