Counting the objects
====================

These objects are also called k-partitions in many places.

We can count them first since we can use this later to make sure our programs are
generating the right number of objects.

The [Stirling numbers of the 2nd kind](https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind)
are counting the number of placements of `n` balls into `b` **non-empty** bins.

We can extend that to the following formula to allow for empty bins
`\sum_{e=0}^{b} {b\choose e} S(n,b-e) (b-e)!`

<insert_img>

In the sum above, `e` represents the number of empty bins, so we're
allowing between `0` and `b` empty bins, the term `binomial(b,e)` will
account for any position of the empty bins, while the remaining `b-e`
non-empty bins are counted by `S(n,b-e)`, but we still need to allow for
all permutations of the non-empty bins which we're doing through `(b-e)!`.

We can count this using the following program:

```python3
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
```

OUTPUT:

```
c(2,2): 4
c(3,3): 27
c(6,7): 117649
```

See also:

* [This thread](https://math.stackexchange.com/a/395046/68328) derives the same formula

* These two threads discuss the probability of having `e` empty bins after placing the balls [link1](https://math.stackexchange.com/a/1877442/68328) , [link2](https://math.stackexchange.com/a/351411/68328)


Generating the objects
======================

Here is a recursive algorithm that generates the placements of balls into bins.
Each ball is placed in one of the bins, then the algorithm recurses further into the
remaining balls to place the next ball. When there are no more balls to place, we're printing
the contents of all bins.

```python3
#!/usr/bin/python3
import string
import copy
#
# This generates all the possible placements of
# b balls into n boxes (including configurations with empty boxes).
#
class BinPartitions:

    def __init__(self, balls, num_bins):
        self.balls = balls
        self.bins = [{} for x in range(num_bins)]

    def print_bins(self, bins):
        L = []
        for b in bins:
            buf = ''.join(sorted(b.keys()))
            L += [buf]
        print(",".join(L))

    def _gen_helper(self,balls,bins):
        if len(balls) == 0:
            self.print_bins(bins)
        else:
            A,B = balls[0],balls[1:]
            for i in range(len(bins)):
                new_bins = copy.deepcopy(bins)
                new_bins[i].update({A:1})
                self._gen_helper(B,new_bins)

    def get_all(self):
        self._gen_helper(self.balls,self.bins)

BinPartitions(string.ascii_uppercase[:3],3).get_all()
#BinPartitions(string.ascii_uppercase[:2],2).get_all()
#BinPartitions(string.ascii_uppercase[:3],3).get_all()
#BinPartitions(string.ascii_uppercase[:6],3).get_all()
```

OUTPUT:

```
ABC,,
AB,C,
AB,,C
AC,B,
A,BC,
A,B,C
AC,,B
A,C,B
A,,BC
BC,A,
B,AC,
B,A,C
C,AB,
,ABC,
,AB,C
C,A,B
,AC,B
,A,BC
BC,,A
B,C,A
B,,AC
C,B,A
,BC,A
,B,AC
C,,AB
,C,AB
,,ABC
```

Other algorithms for generating the objects
===========================================

Partition-based algorithms: [link1](https://stackoverflow.com/a/31639692/827519) ; [link2](https://stackoverflow.com/a/39199937/827519)

Knuth's Algorithm U: [link1](https://codereview.stackexchange.com/a/1944/29883) ; [link2](https://stackoverflow.com/a/52240171/827519) ; [link3](https://stackoverflow.com/q/45829748/827519)


