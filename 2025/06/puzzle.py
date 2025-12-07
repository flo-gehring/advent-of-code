from functools import reduce
f  = open("advent-of-code-input/2025/06/input.txt" )

lines = [ line.split() for line in f.readlines()]
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
