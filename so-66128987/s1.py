#!/usr/bin/python3
from sympy import *
a, b = symbols('a b')
expr = a + a/b + a/b**2 + a**2/b**2 + a/b**3

def truncate(e):
    c = symbols('c')
    e1 = e.subs(S(1)/b,c)
    p = 0
    for m in poly(e1,a,c).monoms():
        exp_a,exp_c = m
        if exp_c <= exp_a:
            p += a**exp_a * (1/b)**exp_c
    return p

truncated_expr = truncate(expr)

print(truncated_expr)

