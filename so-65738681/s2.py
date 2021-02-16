#!/usr/bin/python3
from itertools import permutations
import copy

#
# This is a generator for the placement of k bars among n elements
# 
def bars(n,k,i,L):
    if i == k:
        yield L
    else:
        if len(L) == 0:
            low = -1
        else:
            low = L[i-1]

        for j in range(low+1,n):
            yield from bars(n,k,i+1,L+[j])

#
# In each permutation, we're trying to place the bars in different ways
# and we're printing the results.
#
balls = ['A','B','C']
num_bins = 4
seen = {}
for stars in permutations(balls):
    # print("perm=",p)
    lb = len(balls)

    for bpos in bars(lb+num_bins-1,num_bins-1,0,[]):
        bins = []
        b = set()
        i,j,k=0,0,0
        while i < lb + num_bins-1:
            if j < len(bpos) and i == bpos[j]:
                bins.append(b)
                b = set()
                j += 1
            elif k < lb:
                b.add(stars[k])
                k += 1
            i += 1
        bins.append(b)

        if str(bins) not in seen:
            print(bins)
        seen[str(bins)] = 1


