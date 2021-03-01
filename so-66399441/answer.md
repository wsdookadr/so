> Whenever I substitute this expression into the fraction it fully simplifies the expression, which is not what I want. I just want to replace x with the fraction `a/b` (in this case `2/3` or `1/3` depending on the seed).

It's possible to do this, if we use a `with` expression to [temporarily disable evaluation](https://github.com/sympy/sympy/issues/12017#issuecomment-270311862) for that code block, and then we use [two dummy variables](https://docs.sympy.org/latest/modules/core.html#dummy) in order to represent the fraction, and finally we do the substitution with numerical values.

So the following line in your code:

```python3
pressure_derivative_ab = pressure_derivative.xreplace({ x : Rational(a,b)}) 
```

can be changed to:

```python3
with evaluate(False):
    a1,b1=Dummy('a'),Dummy('b')
    pressure_derivative_ab = pressure_derivative.subs(x,a1/b1).subs({a1: a,b1: b})
```

The expressions `pressure_derivative` and `pressure_derivative_ab` after this are:

[![enter image description here][1]][1]


> How can I make sympy display the full, and not inline version of it's fractions for some of its fractions? In particular I would like the last fraction `1/5` to instead be displayed in full. eg. `\fraction{1}{5}`

For this, you only need to change this line:

```
        = \py{pressure_ab}
```

into this line:

```
        = \py{latex(pressure_ab)}
```

Because we want pythontex to use the sympy [latex printer](https://docs.sympy.org/latest/tutorial/printing.html#mathrm-latex), instead of the [ascii printer](https://docs.sympy.org/latest/tutorial/printing.html#ascii-pretty-printer).


All the code in this post is [also available in this repo](https://github.com/wsdookadr/so/tree/master/so-66399441).

  [1]: https://i.stack.imgur.com/yekjt.png