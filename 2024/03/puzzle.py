import re
input = open("2024/03/input.txt").read()
exp = re.compile("mul\((\\d{1,3}),(\\d{1,3})\)")

splitDos = input.split("do()")
dontsRemoved = [s.split("don't()")[0] if "don't()" in s else s for s in splitDos]

def sumInput(s):
    operands = exp.findall(s)
    return sum([int(op[0]) * int(op[1]) for op in operands])
print(sum([sumInput(s) for s in dontsRemoved]))
