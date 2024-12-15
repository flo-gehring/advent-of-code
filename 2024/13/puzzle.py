path = "2024/13/input.txt"

class Machine:
    def __init__(self, a: tuple[int,int], b: tuple[int,int], prize:tuple[int,int] ):
        self.a = a
        self.b = b
        self.prize = prize


def add_vec(lhs: tuple[int,int], rhs:tuple[int,int]) -> tuple[int,int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])

def scalar_mult(v: tuple[int,int], s:int) -> tuple[int,int]:
    return (int(v[0] * s), (v[1] * s))

input: list[Machine] = []
lines = open(path).readlines()

def read_coords(line: str) -> tuple[int,int]:
    x = int(line[line.index("X")+2:line.index(",")])
    y = int(line[line.index("Y")+2:])
    return (x,y)

for idx, line in list(enumerate(lines))[::4]:
    button_a_line = line
    button_b_line = lines[idx+1]
    prize_line = lines[idx+2]
    input.append(
        Machine(
        read_coords(button_a_line),
        read_coords(button_b_line),
        read_coords(prize_line))
        )

COST_A = 3
COST_B = 1


def get_max_button_presses(button_movement: tuple[int,int], prize: tuple[int,int]):
    upper_bound_by_x = int(prize[0] / button_movement[0]) +1
    upper_bound_by_y = int(prize[1] / button_movement[1]) +1
    return min(upper_bound_by_x, upper_bound_by_y, 100)

def solve_machine_part1(machine: Machine) -> tuple[int,int]:
    max_a_presses = get_max_button_presses(machine.a, machine.prize)
    max_b_presses = get_max_button_presses(machine.b, machine.prize)
    possible_solutions = []
    for a_presses in range(max_a_presses +1):
        for b_presses in range(max_b_presses +1):
            coord = add_vec(scalar_mult(machine.a, a_presses), scalar_mult(machine.b, b_presses))
            if coord == machine.prize:
                possible_solutions.append((a_presses, b_presses))
    return possible_solutions

def calc_cost(moves):
    return COST_A * moves[0] + COST_B * moves[1]

best_solves = []
for machine in input:
    solutions = solve_machine_part1(machine)
    if solutions:
        min_solution =  min(solutions, key= calc_cost)
        best_solves.append(calc_cost(min_solution))
print("Solution 1", sum(best_solves))

new_machines = [Machine(m.a, m.b, add_vec(m.prize, (10000000000000, 10000000000000))) for m in input]

def solve_machine_part1(machine: Machine) -> tuple[int,int]:
    max_a_presses = get_max_button_presses(machine.a, machine.prize)
    max_b_presses = get_max_button_presses(machine.b, machine.prize)
    possible_solutions = []
    for a_presses in range(max_a_presses +1):
        for b_presses in range(max_b_presses +1):
            coord = add_vec(scalar_mult(machine.a, a_presses), scalar_mult(machine.b, b_presses))
            if coord == machine.prize:
                possible_solutions.append((a_presses, b_presses))
    return possible_solutions

