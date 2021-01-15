#!/usr/bin/python3
from symengine import *
x=var("x")
u=Function("g")(x)
v=Function("b")(x)

f = u*v
n = 50
print(f.diff(x,n))
