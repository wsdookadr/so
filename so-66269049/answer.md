There are two common ways to replace functions in an expression(in this case the expression is the matrix `T`). One is to use the [`rewrite`](https://docs.sympy.org/latest/modules/core.html#sympy.core.basic.Basic.replace) function, the other is to use the [`subs`](https://docs.sympy.org/latest/modules/core.html#sympy.core.basic.Basic.subs) function. Any of the two can be used to achieve the same goal of replacing sin/cos with other functions.

In the code below we're replacing the function `s` (which is an alias to `sin`) with the undefined function `s1` (whose symbolic name is `s`).
The same happens with `c` and `c1`.

```python3
from sympy import *

# s,c act as aliases to sin,cos
s = sin
c = cos

# the intended short-hand functions used to replace sin/cos later on
s1 = Function('s')
c1 = Function('c')

a,d,theta,alpha = symbols('a d \\theta \\alpha')

T = Matrix([
    [c(theta), -s(theta), 0, a],
    [s(theta) * c(alpha), c(theta) * c(alpha), -s(alpha), -s(alpha) * d],
    [s(theta) * s(alpha), c(theta) * s(alpha), c(alpha), c(alpha) * d],
    [0, 0, 0, 1]
])

T_1 = T.replace(s,s1).replace(c,c1)
T_2 = T.subs({s:s1,c:c1})

display(T_1)
display(T_2)
```

OUTPUT:

[![enter image description here][1]][1]


The code used in this post is [also available here](https://github.com/wsdookadr/so/tree/master/so-66269049).

  [1]: https://i.stack.imgur.com/8diDp.png