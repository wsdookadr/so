#!/usr/bin/python3
from symengine import *
import pprint
x=var("x")
b=Function("b")(x)
g=Function("g")(x)

b3,b2=b.diff(x,3),b.diff(x,2)
g4,g3=g.diff(x,4),g.diff(x,3)

def set_to_zero(e):
    e = e.subs({b3:0,b2:0,g4:0,g3:0})
    return e

def sum_of_coef(f):
    s = 0
    if f.func == Add:
        for sum_term in f.args:
            # res = 1
            res = sum_term if sum_term.is_Number else 1
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
    charar = [[0] * (power*2) for x in range(power)]
    coef_sum_array = [[0] * (power*2) for x in range(power)]
    charar[0][0] = b
    charar[0][1] = g
    init_printing()
    for i in range(1, power):
        jmax = (i+1)*2
        for j in range(0, jmax):
            c2,c1,c0 = charar[i-1][j-2],charar[i-1][j-1],charar[i-1][j]
            #print(c2,c1,c0)
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
            charar[i][j] = set_to_zero(expand(expr))
            coef_sum_array[i][j] = sum_of_coef(charar[i][j])

    pprint.pprint(Matrix(coef_sum_array))

main()
