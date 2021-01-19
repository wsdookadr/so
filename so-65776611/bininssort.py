#!/usr/bin/python3
from bisect import bisect_left
import sys

def generate_reversed(n):
    return list(range(n))[::-1]

def generate_alternating(n):
    U=[]
    i,j=0,n-1

    k=0
    while i < j:
        U.append(i)
        U.append(j)
        i += 1
        j -= 1

    return U

def bininssort(L):
    n = len(L)
    i,j=0,0
    for i in range(1,n):
        j=i-1
        x=L.pop(i)
        i1=bisect_left(L,x,0,j+1)
        L.insert(i1,x)
    return L

import argparse
arg_parser = argparse.ArgumentParser(description='Tool for estimating growth rates')
arg_parser.add_argument('--type',  dest='type' , action='store', required=True, help='type of input to generate (best|worst)')
arg_parser.add_argument('--size', dest='size', action='store', required=True, type=int, help='size of input to run')

args = arg_parser.parse_args()

if args.type == "reversed":
    L = generate_reversed(args.size)
elif args.type == "alternating":
    L = generate_alternating(args.size)

import time

start = time.time()
bininssort(L)
end = time.time()

print(end-start)

