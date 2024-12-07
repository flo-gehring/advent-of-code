from typing import List
from itertools import permutations, combinations_with_replacement, product
equations = [line.strip() for line in open("2024/07/input.txt")]
equations = [line.split(":") for line in equations]
equations = [(int(eq[0]), [ int(op.strip()) for op in eq[1].split()]) for eq in equations]

def test_op_sequence(test_value: int, operands: List[int], operators: List[str]) -> bool:
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

def testEquations(test_value: int, operands: List[int]) -> bool:
    operators = ["+", "*", "||"]
    op_sequences = list(product(operators, repeat=len(operands)-1)) 
    
    return any([test_op_sequence(test_value, operands, ops) for ops in op_sequences])


true_eqs= [eq for eq in equations if testEquations(eq[0], eq[1])]
print(true_eqs)
true_results = [eq[0] for eq in true_eqs]
print(true_results)
print(sum(true_results))