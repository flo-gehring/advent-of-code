from typing import List, Iterable
from itertools import  product
equations = [line.strip() for line in open("2024/07/input.txt")]
equations = [line.split(":") for line in equations]
equations = [(int(eq[0]), [ int(op.strip()) for op in eq[1].split()]) for eq in equations]

def test_op_sequence(test_value: int, operands: List[int], operators: Iterable[str]) -> bool:
    result = operands[0]
    for (num, op) in zip(operands[1:], operators):
        if op == "+":
            result = result + num
        elif op == "*":
            result = result * num
        elif op == "||":
            result = int(str(result) + str(num))
        else :
            raise Exception("Unknown Op: " + op )
    return test_value == result

def test_equations(test_value: int, operands: List[int], operators=["+", "*", "||"]) -> bool:
    op_sequences = product(operators, repeat=len(operands)-1) 
    return any([test_op_sequence(test_value, operands, ops) for ops in op_sequences])

# Part 1
true_eqs_part1= [eq for eq in equations if test_equations(eq[0], eq[1], operators=["+" ,"*" ])]
true_results_part1 = [eq[0] for eq in true_eqs_part1]
print("Result Part 1: ", sum(true_results_part1))

# Part 2
true_eqs_part2= [eq for eq in equations if test_equations(eq[0], eq[1], operators=["+" ,"*", "||" ])]
true_results_part2 = [eq[0] for eq in true_eqs_part2]
print("Result Part 2: ",  sum(true_results_part2))