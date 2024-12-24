path = "2024/17/input.txt"


def read_register(line: str) -> int:
    return int(line.split(":")[1].strip())
def read_input(path: str) -> tuple[tuple[int,int,int],  list[int]]:
    input = open(path, "r").readlines()
    return (
        (read_register(input[0]), read_register( input[1]),  read_register(input[2])),
        [int(opcode) for opcode in input[4].split(":")[1].strip().split(",")]
    )

initial_registers, programm = read_input(path)

def run_programm(registers: tuple[int,int,int], programm: list[int]) -> list[int]:
    programm_counter = 0
    programm_length = len(programm)
    (reg_a, reg_b, reg_c) = registers
    output = []
    while programm_counter < programm_length:
        opcode = programm[programm_counter]
        operand = programm[programm_counter + 1] if programm_counter + 1 < len(programm) else None
        current_registers = (reg_a, reg_b, reg_c)
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
    return output         

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
print(",".join([str(x) for x in run_programm(initial_registers, programm)]))