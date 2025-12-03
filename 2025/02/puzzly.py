f  = open("advent-of-code-input/2025/02/input.txt" )
ranges =[(r.split("-")[0], r.split("-")[1]) for r in f.readline().split(",")]

invalid = []
for (start, end) in ranges:
    for id in range(int(start), int(end) +1):
        std_id = str(id)
        half = len(std_id)//2
        if(std_id[:half] == std_id[half:]):
            invalid.append(id)

print(invalid)
print(sum(invalid))
# 2852758602448360

invalid = []
for (start, end) in ranges:
    for id in range(int(start), int(end) +1):
        std_id = str(id)
        length = len(std_id)
        half = length //2
        for i in range(1, half +1):
            if length % i == 0:
                pattern = length // i
                if std_id[:i] * pattern == std_id:
                    invalid.append(id)
                    break

print(invalid)
print(sum(invalid))
# 2852758602448360