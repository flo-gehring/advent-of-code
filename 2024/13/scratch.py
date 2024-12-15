from sympy import symbols

from sympy.matrices import Matrix


A = Matrix([[94, 22], [34, 67]])
b = Matrix([8400,5400])
print(A.solve(b))