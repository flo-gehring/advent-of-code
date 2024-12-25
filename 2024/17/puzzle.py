from dataclasses import dataclass
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
# Test bis 6888574 hat nichts gebrachtl
#print("Solution 2", puzzle2(initial_registers, programm) ) 


def compute_greedy(programm):
    current_byte = 0
    reversed_programm = list( reversed(programm))
    last_computed_value = dict()
    current_a = 0
    while current_byte < len(programm):
        current_a = current_a << 3
        next_byte = get_next_byte_for_output(
            reversed_programm[current_byte],
            current_a,
            programm,
            last_computed_value[current_byte] +1 if current_byte in last_computed_value else 0
        )
        if not next_byte:
            print("Next Byte not possible", current_byte)
            if current_byte in last_computed_value:
                last_computed_value.pop(current_byte)
            current_byte -= 1
            current_a = current_a >> 6
            if current_byte < 0:
                raise Exception("Current Byte Fell below 0 no solution possible")
        else:
            last_computed_value[current_byte] = next_byte
            current_a = current_a|next_byte
            output = run_programm((current_a, 0,0), programm)
            mismatch = [ x[0] for x in enumerate(zip(output, programm)) if x[1][0] != x[1][1]]
            while mismatch:
                current_a= try_correct(current_a, programm, mismatch[0])
                if not current_a:
                    if current_byte in last_computed_value:
                        last_computed_value.pop(current_byte)
                    current_byte -= 1
                    continue
                output = run_programm((current_a, 0,0), programm)
                mismatch =  [ x[0] for x in enumerate(zip(output, programm)) if x[1][0] != x[1][1]]
            
            current_byte += 1
    return current_a


def try_correct(a, programm, index):
    a_1 = (a >> (index * 3 +1)) << 3
    next_byte = get_next_byte_for_output(programm[index], a_1, programm)
    if next_byte:
        mask = ~(~0  << index)
        return ((a_1 | next_byte ) << index)  |  (a & mask)




def puzzle2(programm):
    return compute_greedy(programm)
    




def get_next_byte_for_output(output, current_a, programm, start=0): 
    for b in range(start, 256):
       next_a = current_a | b
       out = run_programm((next_a, 0,0), programm[:-2])
       if out[-1] == output:
           return b
    return None 
    


a = puzzle2(programm)
output = run_programm((a,0,0), programm)
print("P", programm)
print("O", output)
print("Len Prog", len(programm), "Mismatch", [ x[0] for x in enumerate(zip(output, programm)) if x[1][0] != x[1][1]])