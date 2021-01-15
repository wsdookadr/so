from sympy import *
import matplotlib.pyplot as plt
import re
import math
import numpy as np
import time
np.set_printoptions(suppress=True)
# #!/usr/bin/python3

x = Symbol('x')
b = Function('b')(x)
g = Function('g')(x)

b3,b2=b.diff(x,3),b.diff(x,2)
g4,g3=g.diff(x,4),g.diff(x,3)

def set_to_zero(expression):
    expression = expression.subs({b3:0,b2:0,g4:0,g3:0})
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

from functools import lru_cache

def d_ij(charar,i,j,k):


    if(not hasattr(d_ij, "doit")):
        @lru_cache(maxsize=999999)
        def doit(i,j,k):
            if isinstance(charar[i,j], int):
                return 0
            return charar[i,j].diff(x,k)
        d_ij.doit = doit

    #print(i,j,k)
    #print(d_ij.doit.cache_info())
    return d_ij.doit(i,j,k)

#             
#     c2 c1 c0
#  c2 c1 c0
# 
#

def main():
    power = 8
    charar = np.zeros((power, power*2), dtype=Symbol)
    coef_sum_array = np.zeros((power, power*2))
    charar[0,0] = b
    charar[0,1] = g
    coef_sum_array[0,0] = 1
    coef_sum_array[0,1] = 1

    init_printing()

    for i in range(1, power):
        jmax = (i+1)*2
        for j in range(0, jmax):
            start_time = time.time()
            c2,c1,c0 = charar[i-1,j-2],charar[i-1,j-1],charar[i-1,j]
            if   j == 0:
                c01,c02 = d_ij(charar,i-1,j,1),d_ij(charar,i-1,j,2)
                expr =                         b*c01 + g*c02
            elif j == 1:
                c01,c02 = d_ij(charar,i-1,j,1),d_ij(charar,i-1,j,2)
                c11 =     d_ij(charar,i-1,j-1,1)
                expr =        b*c1 + 2*g*c11 + b*c01 + g*c02
            elif j == jmax-2:
                c11 =     d_ij(charar,i-1,j-1,1)
                expr = g*c2 + b*c1 + 2*g*c11
            elif j == jmax-1:
                expr = g*c2
            else:
                c01,c02 = d_ij(charar,i-1,j,1),d_ij(charar,i-1,j,2)
                c11 =     d_ij(charar,i-1,j-1,1)
                expr = g*c2 + b*c1 + 2*g*c11 + b*c01 + g*c02

            charar[i,j] = set_to_zero(expand(expr))
            #pprint("({0},{1})->".format(i,j) + str (charar[i,j]))
            #print(i,j,len(charar[i,j].args))
            print("--- %0.5f seconds for expression---" % (time.time() - start_time))
            start_time = time.time()
            coef_sum_array[i,j] = sum_of_coef(charar[i,j])
            print("--- %0.5f seconds for coeffiecients---" % (time.time() - start_time))

    # pprint(Matrix(coef_sum_array.tolist()))
    pprint(coef_sum_array)

main()


