
from functools import reduce
input = [l.strip().split() for l in  open("2024/02/input.txt").readlines()]
input = [[int(i) for i in line] for line in input]

def report_safe(report):
    if checkSafePrimitiv(report):
        return True
    else: 
        return tryRecover(report)

def tryRecover(report: list):
    for i in range(len(report)):
        rc = report.copy()
        rc.pop(i)
        if checkSafePrimitiv(rc):
            return True
    return False

def checkSafePrimitiv(report):
    diff = [report[i] - report[i+1] for i in range(len(report)-1)]
    greaterZero = [ i > 0 for i in diff]
    lessThanZero = [i < 0 for i in diff]
    allGreater = reduce(lambda a,b: a and b, greaterZero, True)
    maxStepSizeOk = reduce(lambda a,b: a and b, [abs(d) <= 3 for d in diff], True)
    allLower = reduce(lambda a,b: a and b, lessThanZero, True)
    return (allGreater or allLower) and maxStepSizeOk
   
safe = [report_safe(r) for r in input]
print(sum(safe))