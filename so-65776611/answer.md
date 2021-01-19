You can write binary insertion sort easily by leveraging built-in functions such as [`bisect_left`](https://docs.python.org/3/library/bisect.html#bisect.bisect_left) and [`list.pop(..)`](https://docs.python.org/3/tutorial/datastructures.html) and [`list.insert(..)`](https://docs.python.org/3/tutorial/datastructures.html) :

```python3
def bininssort(L):
    n = len(L)
    i,j=0,0
    for i in range(1,n):
        j=i-1
        x=L.pop(i)
        i1=bisect_left(L,x,0,j+1)
        L.insert(i1,x)
    return L
```

About the worst-case, since at the `i-th` iteration of the loop, we perform a binary search inside the sub-array `A[0..i]`, with `0<=i<n`, that should take `log(i)` operations, so we now know we have to insert an element at location `i1` and we insert it, but the insertion means we have to push all the elements that follow it one position to the right, and that's at least `n-i` operations (it can be more than `n-i` operations depending on the insertion location). If we sum up just these two we get `\sum_{i=1}^n log(i) + (n-i) = log(n!) + (n*(n+1))/2 ~ n*log(n) + (n*(n+1))/2`

(in the above [Stirling's approximation](https://en.wikipedia.org/wiki/Stirling%27s_approximation) of `log(n!)` is being used)


Now [the wiki page](https://en.wikipedia.org/wiki/Analysis_of_algorithms) says

> As a rule-of-thumb, one can assume that the highest-order term in any given function dominates its rate of growth and thus defines its run-time order

So I think the conclusion would be that in the worst-case the binary insertion sort has `O(n^2)` complexity.

See also:
- [insertion sort using binary search](https://stackoverflow.com/q/50360582/827519)
- [insertion sort with binary search](https://stackoverflow.com/questions/18022192/insertion-sort-with-binary-search)
- [analysis of binary insertion sort](https://cboard.cprogramming.com/cplusplus-programming/139831-analysis-binary-insertion-sort-algorithm.html)
- [binary insertion sort and complexity](https://stackoverflow.com/q/42564936/827519)


Then I tried to check how it's performing on reversed(`n,n-1,n-2,..,1`) and alternating (`0,n-1,1,n-2,2,n-3,...`) lists. And I fitted them (using the [matchgrowth module](https://pypi.org/project/matchgrowth/)) to different growth rates, this part is just an approximation. The reversed order was fitted to polynomial time, and the alternating order was fitted to quasilinear time


[![enter image description here][1]][1]



The code used here [is available](https://github.com/wsdookadr/so/tree/master/so-65776611) in this repository.


  [1]: https://i.stack.imgur.com/s100g.png