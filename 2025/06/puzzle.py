from functools import reduce
path = "advent-of-code-input/2025/06/input.txt"
f  = open( path)
input_lines = f.readlines()

lines = [ line.split() for line in input_lines]
transposed_input = [list(x) for x in zip(*lines)] # thank you, stack overflow https://stackoverflow.com/questions/21444338/transpose-nested-list-in-python


total = 0
for problem in transposed_input:
    numbers = [int(i) for i in problem[:-1]]
    if(problem[-1] == "+"):
        total += sum(numbers)
    elif problem[-1] == "*":
        total += reduce(lambda x,y: x * y, numbers,1 )
    else:
        raise Exception("Unknown operatpr")
print(total)


# part 2
total = 0
operators = input_lines[-1]
operand_table = input_lines[:-1]
transposed_operand_table = [list(x) for x in zip(*operand_table)]

operator_index = 0
current_operands = []

def get_next_operator_index(operators: list[str], current_index:int):
    for (idx, ch) in enumerate(operators[current_index+1:]):
        if ch.strip() != "":
            return current_index + idx +1

for operand in transposed_operand_table:
    if all([x.strip() == "" for x in operand]):
        operator = operators[operator_index]
        if(operator == "+"):
            total += sum(current_operands)
        elif operator == "*":
            total += reduce(lambda x,y: x * y, current_operands,1 )
        else:
            raise Exception("Unknown operatpr")
        
        current_operands = []
        operator_index = get_next_operator_index(operators, operator_index)
    else:
        current_operands.append(int("".join(operand)))



print(total)