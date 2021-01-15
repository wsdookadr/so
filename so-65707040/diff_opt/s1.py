#!/usr/bin/python3
from sympy import *
x = symbols('x')
u = Function('u')(x)
v = Function('v')(x)
f = u * v
n = 50

f1 = f.diff(x,n)
print(f1)
