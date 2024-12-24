from dataclasses import dataclass
path = "2024/17/input_test.txt"


def read_register(line: str) -> int:
    return int(line.split(":")[1].strip())
def read_input(path: str) -> tuple[tuple[int,int,int],  list[int]]:
    input = open(path, "r").readlines()
    return (
        (read_register(input[0]), read_register( input[1]),  read_register(input[2])),
        [int(opcode) for opcode in input[4].split(":")[1].strip().split(",")]
    )

initial_registers, programm = read_input(path)

@dataclass
class State:
    programmCounter: int
    registers: tuple[int,int]
    output: list[int]


def step(programm: list[int], state:State) -> State:
        programm_counter = state.programmCounter
        opcode = programm[programm_counter]
        operand = programm[programm_counter + 1] if programm_counter + 1 < len(programm) else None
        current_registers = state.registers
        (reg_a, reg_b, reg_c) = state.registers
        output = state.output
        match opcode:
            case 0: # A-Division
                reg_a = perform_division(operand, current_registers)
            case 1: # bitwise xor
                lhs  = reg_b
                rhs = operand
                reg_b = lhs ^ rhs
            case 2: # mod 8 to b
                reg_b = resolve_combo(operand, current_registers ) % 8
            case 3: # Jump if a not zero
                programm_counter =  operand - 2 if reg_a != 0 else programm_counter
            case 4:# Reg b xor reg c
                reg_b = reg_b ^ reg_c
            case 5:
                output.append(resolve_combo(operand, current_registers) % 8)
            case 6:
                reg_b = perform_division(operand, current_registers)
            case 7:
                reg_c = perform_division(operand, current_registers)
        programm_counter += 2
        return State(programm_counter, (reg_a, reg_b, reg_c), output)

def run_programm(registers: tuple[int,int,int], programm: list[int]) -> list[int]:
    programm_length = len(programm)
    state = State(
        0,
        registers,
        []
    )
    while state.programmCounter < programm_length:
        state = step(programm, state)
    return state.output     


def can_equal(programm: list[int], output: list[int]):
    if len(output)  > len(programm):
        return False
    return programm[:len(output)] == output
    
def  test_programm(registers, programm ) -> bool:
    programm_length = len(programm)
    state = State(
        0,
        registers,
        []
    )
    while True:
        state = step(programm, state)
        has_halted = state.programmCounter >= programm_length
        if has_halted  :
            return state.output == programm
        elif not can_equal(programm, state.output):
            return False

def puzzle2(registers, programm):
    initial_register_a = 0
    while True:
        print("Test", initial_register_a)
        if test_programm((initial_register_a, registers[1], registers[2]), programm ):
            return initial_register_a
        initial_register_a += 1

def perform_division(operand, registers ):
    numerator =  registers[0]
    combo = resolve_combo(operand, registers)
    denominator = float(2**combo)
    return int(numerator / denominator)

def resolve_combo(opcode: int, registers: tuple[int,int,int]) -> int:
    if opcode <= 3:
        return opcode
    elif opcode <= 6:
        return registers[opcode - 4]
    else:
        raise Exception(f"Unknown Opcode {opcode}") 

print(initial_registers)
print(programm)
print("Solution 1", ",".join([str(x) for x in run_programm(initial_registers, programm)]))
print("Solution 2", puzzle2(initial_registers, programm) )