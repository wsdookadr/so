Overview
--------

So, there are two formulas about derivatives that are interesting here:
1) [Faa di Bruno's formula](https://en.wikipedia.org/wiki/Fa%C3%A0_di_Bruno%27s_formula) which is a way to quickly find the n-th derivative of `f(g(x))` , and looks a lot like the [Multinomial theorem](https://en.wikipedia.org/wiki/Multinomial_theorem)
2) The [General Leibniz rule](https://en.wikipedia.org/wiki/General_Leibniz_rule) which is a way to quickly find the n-th derivative of `f(x)*g(x)` and looks a lot like the [Binomial theorem](https://en.wikipedia.org/wiki/Binomial_theorem)

Both of these have been discussed in [pull request #13892](https://github.com/sympy/sympy/pull/13892#issuecomment-357240042) the n-th derivative was sped up using the general Leibniz rule.

> I'm trying to see how fast the coefficients of the expression are growing

In your code, the general formula for computing `c[i][j]` is this:

`c[i][j] = g * c[i-1][j-2] + b * c[i-1][j-1] + 2 * g * c'[i-1][j-1] + g * c''[i-1][j]`

(where by `c'[i][j]` and `c''[i][j]` are the 1st and 2nd derivatives of `c[i][j]`)

Because of this, and by the Leibniz rule mentioned above, I think intuitively, the coefficients computed should be related to [Pascal's triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle) (or at the very least they should have some combinatorial relation).

Optimization #1
---------------

In the original code, the function `sum_to_coef(f)` serializes the expression `f` to a string and then discarding everything that doesn't look like a number, and then sums the remaining numbers.

We can avoid serialization here by just traversing the expression tree and collecting what we need

```python3
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
```

Optimization #2
---------------

In the function `set_to_zero(expr)` all the 2nd and 3rd derivatives of `b`, and the 3rd and 4th derivatives of `g` are replaced by zero.

We can collapse all those substitutions into one statement like so:

```python3
b3,b2=b.diff(x,3),b.diff(x,2)
g4,g3=g.diff(x,4),g.diff(x,3)

def set_to_zero(expression):
    expression = expression.subs({b3:0,b2:0,g4:0,g3:0})
    return expression
```

Optimization #3
----------------

In the original code, for every cell `c[i][j]` we're calling `simplify`. This turns out to have a big impact on performance but actually we can skip this call, because fortunately our expressions are just sums of products of derivatives or unknown functions.

So the line

```python3
charar[i,j] = set_to_zero(expand(simplify(expr)))
```

becomes

```python3
charar[i,j] = set_to_zero(expand(expr))
```

Optimization #4
----------------

The following was also tried but turned out to have very little impact.

For two consecutive values of j, we're computing `c'[i-1][j-1]` twice.

```                                                
j-1       c[i-1][j-3] c[i-1][j-2] c[i-1][j-1]
  j                   c[i-1][j-2] c[i-1][j-1] c[i-1][j]
```

If you look at the loop formula in the `else` branch, you see that `c'[i-1][j-1]` has already been computed. It can be cached, but this optimization
has little effect in the SymPy version of the code.

Here it's also important to mention that it's [possible to visualize](https://stackoverflow.com/a/65147704/827519) the call tree of SymPy involved in computing these derivatives. It's actually larger, but here is part of it:

[![nth derivative call tree][1]][1]

We can also generate a flamegraph using the [py-spy](https://github.com/benfred/py-spy) module just to see where time is being spent:

[![flamegraph][2]][2]

As far as I could tell, 34% of the time spent in `_eval_derivative_n_times` , 10% of the time spent in the function `getit` from `assumptions.py` , 12% of the time spent in `subs(..)` , 12% of the time spent in `expand(..)` 


Optimization #5
----------------

Apparently when [pull request #13892](https://github.com/sympy/sympy/pull/13892#issuecomment-357240042) was merged into SymPy, it also introduced a performance regression.

In one of the [comments regarding that regression, Ondrej Certik recommends](https://github.com/sympy/sympy/issues/14674#issuecomment-539249502) using SymEngine to improve performance of code that makes heavy use of derivatives.

So I've ported the code mentioned to [SymEngine.py](https://github.com/symengine/symengine.py) and noticed that it runs **98 times faster** than the SymPy version for `power=8` ( and **4320** times faster for `power=30`)

The required module can be installed via `pip3 install --user symengine`.


```python3
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
    power = 8
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
```


Performance after optimization #5
---------------------------------

I think it would be very interesting to look at the number of terms in `c[i][j]` to determine how quickly the expressions are growing. That would definitely help in estimating the complexity of the current code.

But for practical purposes I've plotted the current time and memory consumption of the SymEngine code above and managed to get the following chart: 

![performance_modif6][3]

Both the time and the memory seem to be growing polynomially with the input (the `power` parameter in the original code).

The same chart but as a [log-log plot](https://en.wikipedia.org/wiki/Log%E2%80%93log_plot) can be viewed here:

![performance_modif6_loglog][4]

Like the [wiki page](https://en.wikipedia.org/wiki/Log%E2%80%93log_plot#Relation_with_monomials) says, a straight line on a log-log plot corresponds to a monomial. [This offers a way to recover](https://math.stackexchange.com/a/3245780/68328) the exponent of the monomial.

So if we consider two points N=16 and N=32 between which the log-log plot is definitely a straight line

```python3
import pandas as pd
df=pd.read_csv("modif6_bench.txt", sep=',',header=0)

def find_slope(col1,col2,i1,i2):
    xData = df[col1].to_numpy()
    yData = df[col2].to_numpy()
    
    x0,x1 = xData[i1],xData[i2]
    y0,y1 = yData[i1],yData[i2]
    
    m = log(y1/y0)/log(x1/x0)
    return m

print("time slope = {0:0.2f}".format(find_slope("N","time",16,32)))
print("memory slope = {0:0.2f}".format(find_slope("N","memory",16,32)))
```

Output:

```
time slope = 5.69
memory slope = 2.62
```

So very rough approximation of [time complexity](https://en.wikipedia.org/wiki/Time_complexity) would be `O(n^5.69)` and an approximation of [space complexity](https://en.wikipedia.org/wiki/Space_complexity) would be `O(2^2.62)`.

Performance with defined `b` and `g` functions
----------------------------------------------

In the first original code block, the functions `b` and `g` were undefined functions. This means SymPy and SymEngine didn't know anything about them.

The 2nd original code block defines `b=1+x` and `g=1+x+x**2` . If we run all of this again with known `b` and `g` the code runs much faster, and the running time curve and the memory usage curves are better than with unknown functions

[![enter image description here][5]][5] 

[![enter image description here][6]][6]


```
time slope = 2.95
memory slope = 1.35
```

Other notes
-----------

If you run this for `power=8` the coefficients will look like this:

```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[1, 5, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[1, 17, 40, 31, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[1, 53, 292, 487, 330, 106, 16, 1, 0, 0, 0, 0, 0, 0, 0, 0]
[1, 161, 1912, 6091, 7677, 4693, 1520, 270, 25, 1, 0, 0, 0, 0, 0, 0]
[1, 485, 11956, 68719, 147522, 150706, 83088, 26573, 5075, 575, 36, 1, 0, 0, 0, 0]
[1, 1457, 73192, 735499, 2568381, 4118677, 3528928, 1772038, 550620, 108948, 13776, 1085, 49, 1, 0, 0]
[1, 4373, 443524, 7649215, 42276402, 102638002, 130209104, 96143469, 44255170, 13270378, 2658264, 358890, 32340, 1876, 64, 1]
```

So as it turns out, the 2nd column coincides with [A048473](http://oeis.org/A048473) which according to OEIS is *"The number of triangles (of all sizes, including holes) in Sierpiński's triangle after n inscriptions"*.


All the code for this is also available in [this repo](https://github.com/wsdookadr/so/tree/master/so-65707040).


  [1]: https://i.stack.imgur.com/q58FS.png
  [2]: https://i.stack.imgur.com/tJBbl.png
  [3]: https://i.stack.imgur.com/cV19w.png
  [4]: https://i.stack.imgur.com/YSgFD.png
  [5]: https://i.stack.imgur.com/qFe4g.png
  [6]: https://i.stack.imgur.com/sqELH.png