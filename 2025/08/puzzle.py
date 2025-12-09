from dataclasses import dataclass
from math import sqrt
from functools import reduce

base_path = "advent-of-code-input/2025/08/" 
test_input = True
path = base_path + ("test.txt" if test_input else "input.txt")
f  = open( path)

@dataclass
class vector:
    id: str
    x:int
    y: int
    z: int

    def dist(self, other) -> float:
        x_diff = other.x - self.x
        y_diff = other.y - self.y
        z_diff = other.z - self.z 
        return sqrt( x_diff**2 + y_diff**2 + z_diff**2)

vectors = [
    vector(str(l[0]), int(l[1][0]), int(l[1][1]) , int(l[1][2])) for l in enumerate([  line.split(",") for line in f.readlines()])
]


distances: list[tuple[tuple[int,int], float]] = []
for vecIdx1 in range(len(vectors)):
    for vecIdx2 in range(vecIdx1 +1, len(vectors)):
        if vecIdx1 == vecIdx2:
            continue
        vec1 = vectors[vecIdx1]
        vec2 = vectors[vecIdx2]
        distances.append(
            ((vec1.id, vec2.id), vec1.dist(vec2))
        )

distances.sort(key=lambda x: x[1])

num_to_connect = 10 if test_input else 1000
num_connected = 0

circuits = [
    set( [vec.id]) for vec in vectors
]


def find_circuit(id):
    for c in circuits:
        if id in c:
            return c
    raise Exception(f"Id {id} not found" )
def merge_circuits(id1, id2):
    circuit1 = find_circuit(id1)
    circuit2 = find_circuit(id2)
    if circuit1 is circuit2:
        return
    circuits.remove(circuit1)
    circuits.remove(circuit2)
    circuits.append(circuit1.union(circuit2))


for i in range(num_to_connect):
    (vec1, vec2) = distances[i][0]
    merge_circuits(vec1, vec2)
    

cicuit_len = [
    len(c) for c in circuits
]

cicuit_len.sort(reverse=True)
print(cicuit_len)
top_n = cicuit_len[:3]
print("Part 1", reduce(lambda x,y: x*y,top_n, 1))


vec1 = None
vec2 = None
for i in range(num_to_connect, len(distances)):
    (vec1, vec2) = distances[i][0]
    merge_circuits(vec1, vec2)
    if(len(circuits) == 1):
        break

print("Part2", vectors[int(vec1)].x *vectors[int(vec2)].x )
        

    
