#!/usr/bin/python3

from sympy import *
import matplotlib.pyplot as plt
import re
import math
import numpy as np
import time
np.set_printoptions(suppress=True)

x = Symbol('x')
b = Function('b')(x)
g = Function('g')(x)

def set_to_zero(expression):
    expression = expression.subs(Derivative(b, x, x, x), 0)
    expression = expression.subs(Derivative(b, x, x), 0)
    expression = expression.subs(Derivative(g, x, x, x, x), 0)
    expression = expression.subs(Derivative(g, x, x, x), 0)
    return expression

def sum_of_coef(f):
    s = 0
    if f.func == Add:
        for sum_term in f.args:
            res = 1
            if len(sum_term.args) == 0:
                s += res
                continue
            first = sum_term.args[0]
            if first.is_Number == True:
                res = first
            else:
                res = 1
            s += res
    elif f.func == Mul:
        first = f.args[0]
        if first.is_Number == True:
            s = first
        else:
            s = 1
    elif f.func == Pow:
        s = 1
    return s

def main():
    power = 4
    charar = np.zeros((power, power*2), dtype=Symbol)
    coef_sum_array = np.zeros((power, power*2))
    charar[0,0] = b
    charar[0,1] = g
    coef_sum_array[0,0] = 1
    coef_sum_array[0,1] = 1


    for i in range(1, power):
        jmax = (i+1)*2
        for j in range(0, jmax):
            start_time = time.time()
            c2,c1,c0 = charar[i-1,j-2],charar[i-1,j-1],charar[i-1,j]

            if   j == 0:
                expr =                                b*c0.diff(x) + g*c0.diff(x,2)
            elif j == 1:
                expr =        b*c1 + 2*g*c1.diff(x) + b*c0.diff(x) + g*c0.diff(x,2)
            elif j == jmax-2:
                expr = g*c2 + b*c1 + 2*g*c1.diff(x)
            elif j == jmax-1:
                expr = g*c2
            else:
                expr = g*c2 + b*c1 + 2*g*c1.diff(x) + b*c0.diff(x) + g*c0.diff(x,2)

            charar[i,j] = set_to_zero(expand(simplify(expr)))
            print("--- %0.5f seconds for expression---" % (time.time() - start_time))
            start_time = time.time()
            coef_sum_array[i,j] = sum_of_coef(charar[i,j])
            print("--- %0.5f seconds for coeffiecients---" % (time.time() - start_time))

    pprint(Matrix(coef_sum_array.tolist()))

main()

