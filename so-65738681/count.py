#!/usr/bin/python3
from sympy import *
from sympy.functions.combinatorial.numbers import stirling

#
# Counting the number of ways to place n balls into b boxes, allowing
# for empty boxes.
#


def count_k_partitions(n,b):
    ans = 0
    for e in range(0,b+1):
        ans += binomial(b,e) * stirling(n,b-e,kind=2) * factorial(b-e)
    return ans

print("c(2,2):",count_k_partitions(2,2))
print("c(3,3):",count_k_partitions(3,3))
print("c(6,7):",count_k_partitions(6,7))
