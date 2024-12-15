from dataclasses import dataclass
from functools import reduce
import os

test = True
path = "2024/14/input_test.txt" if test else "2024/14/input.txt"
bounds = (11,7) if test else (101,103)

@dataclass
class Robot:
    position: tuple[int,int]
    velocity: tuple[int,int]

    def move(self, seconds: int, input_bounds: tuple[int,int]) :
        new_position = add_vec(self.position, scalar_mult(self.velocity, seconds))
        return Robot(
            (new_position[0] % input_bounds[0], new_position[1] % input_bounds[1]),
            self.velocity
        )

def add_vec(lhs: tuple[int,int], rhs:tuple[int,int]) -> tuple[int,int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])

def scalar_mult(v: tuple[int,int], s:int) -> tuple[int,int]:
    return (int(v[0] * s), (v[1] * s))

def parse_robot(line: str) -> Robot:
    s = line.split()
    pos = s[0][2:].split(",")
    vel =s[1][2:].split(",")

    (p1, p2) = int(pos[0]), int(pos[1])
    (v1, v2) = int(vel[0]), int(vel[1])
    return Robot(
        (p1,p2),
        (v1, v2)
    )


puzzle_in = [
    parse_robot(line.strip()) for line in open(path).readlines()
]

def draw_robots(robots: list[Robot], bounds: tuple[int,int]) -> str:
    positions = [[0 for _ in range(bounds[0])] for _ in range(bounds[1])]
    for robot in robots:
        positions[robot.position[1]][robot.position[0]] += 1
    
    result = ""
    for row in positions:
        for cell in row:
            result += str(cell) if cell != 0 else "." 
        result += "\n"
    return result

moved = [r.move(100, bounds) for r in puzzle_in]

if test:   
    print(draw_robots(puzzle_in, bounds))
    print(draw_robots(moved, bounds))


def count_robots_in_quadrant(robots: list[Robot], input_bound: tuple[int,int], quadrant: int) -> int:
    assert quadrant >= 0 and quadrant <= 3
    x_quadrant  = quadrant % 2
    y_quadrant = int(quadrant / 2)
    x_min = 0 if x_quadrant == 0 else ((int(input_bound[0] / 2) + 1))

    y_min = 0 if y_quadrant == 0 else (int(input_bound[1] / 2) + 1) 
    x_max = int(input_bound[0] / 2)-1 if x_quadrant == 0 else input_bound[0]
    y_max= int(input_bound[1] / 2)-1 if y_quadrant == 0 else input_bound[1]
    return sum([1 for robot in robots if robot.position[0] <= x_max and robot.position[0] >= x_min and robot.position[1] <= y_max and robot.position[1] >= y_min])

print("Solution 1",  reduce(lambda x,y: x * y, [count_robots_in_quadrant(moved,bounds, quadrant ) for quadrant in range(4)]))


for i in range(300):
    moved = [r.move(i, bounds) for r in puzzle_in]
    print("-----------------")
    print(draw_robots(moved, bounds))
    print("Second", i)
    input("Press enter to continue")
    os.system('cls' if os.name == 'nt' else 'clear')
