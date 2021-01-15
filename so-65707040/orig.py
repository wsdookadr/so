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

def new_coef(gamma, beta, coef_minus2, coef_minus1, coef):
    return expand(simplify(gamma*coef_minus2 + beta*coef_minus1 + 2*gamma*coef_minus1.diff(x)\
            +beta*coef.diff(x)+gamma*coef.diff(x,2)))
def new_coef_first(gamma, beta, coef):
    return expand(simplify(beta*coef.diff(x)+gamma*coef.diff(x,2)))
def new_coef_second(gamma, beta, coef_minus1, coef):
    return expand(simplify(beta*coef_minus1 + 2*gamma*coef_minus1.diff(x)\
            +beta*coef.diff(x)+gamma*coef.diff(x,2)))
def new_coef_last(gamma, beta, coef_minus2):
    return lambda x: gamma(x)*coef_minus2(x)
def new_coef_last(gamma, beta, coef_minus2):
    return expand(simplify(gamma*coef_minus2 ))
def new_coef_second_to_last(gamma, beta, coef_minus2, coef_minus1):
    return expand(simplify(gamma*coef_minus2 + beta*coef_minus1 + 2*gamma*coef_minus1.diff(x)))

def set_to_zero(expression):
    expression = expression.subs(Derivative(b, x, x, x), 0)
    expression = expression.subs(Derivative(b, x, x), 0)
    expression = expression.subs(Derivative(g, x, x, x, x), 0)
    expression = expression.subs(Derivative(g, x, x, x), 0)
    return expression

def sum_of_coef(expression):
    sum_of_coef = 0
    for i in str(expression).split(' + '):
        if i[0:1] == '(':
            i = i[1:]
        integers = re.findall(r'\b\d+\b', i)
        if len(integers) > 0:
            length_int = len(integers[0])
            if i[0:length_int] == integers[0]:
                sum_of_coef += int(integers[0])
            else:
                sum_of_coef += 1
        else:
            sum_of_coef += 1
    return sum_of_coef
power = 4
charar = np.zeros((power, power*2), dtype=Symbol)
coef_sum_array = np.zeros((power, power*2))
charar[0,0] = b
charar[0,1] = g
coef_sum_array[0,0] = 1
coef_sum_array[0,1] = 1
for i in range(1, power):
    #print(i)
    for j in range(0, (i+1)*2):
        #print(j, ':')
        #start_time = time.time()
        if j == 0:
            charar[i,j] = set_to_zero(new_coef_first(g, b, charar[i-1, j]))
        elif j == 1:
            charar[i,j] = set_to_zero(new_coef_second(g, b, charar[i-1, j-1], charar[i-1, j]))
        elif j == (i+1)*2-2:
            charar[i,j] = set_to_zero(new_coef_second_to_last(g, b, charar[i-1, j-2], charar[i-1, j-1]))
        elif j == (i+1)*2-1:
            charar[i,j] = set_to_zero(new_coef_last(g, b, charar[i-1, j-2]))
        else:
            charar[i,j] = set_to_zero(new_coef(g, b, charar[i-1, j-2], charar[i-1, j-1], charar[i-1, j]))
        #print("--- %s seconds for expression---" % (time.time() - start_time))
        #start_time = time.time()
        coef_sum_array[i,j] = sum_of_coef(charar[i,j])
        #print("--- %s seconds for coeffiecients---" % (time.time() - start_time))

pprint(coef_sum_array)
