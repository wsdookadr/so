Yes, it's possible to apply [Woodbury's identity](https://en.wikipedia.org/wiki/Woodbury_matrix_identity#Discussion). In the code below, the identity is applied on `(I + Phi^T * Phi)**(-1)`. 

The particular case used was `(I+UV)^-1 = I - U*(I+VU)^-1*V`


```python3
from sympy.simplify.simplify import nc_simplify
from sympy import *
N,M,sigma = symbols("N M \sigma")
Phi = MatrixSymbol("Phi", N, M)
In,Im = Identity(N), Identity(M)

f = (Im + Phi.transpose()@Phi).inverse()
f = f @ Phi.transpose()
f = Phi @ f
f = In - sigma**(-2)*f
f = sigma**(-2)*Phi.transpose()@f
f = f@ Phi


def apply_woodburry_1(e,U,V):
    # The Woodbury identity
    #
    # (I+UV)^-1 = I - U * (I+VU)^-1 * V
    # 
    # Below, P will be LHS and Q will be RHS
    #
    UV_dim = (U * V).shape
    I1 = Identity(UV_dim[0])
    VU_dim = (V * U).shape
    I2 = Identity(VU_dim[0])
    
    P = (I1+U*V)**(-1)
    Q = I1 - U * ( (I2+V*U)**(-1) ) * V
    
    return e.replace(P,Q)


display(f)
f = apply_woodburry_1(f,Phi.transpose(),Phi)
display(f)
f = nc_simplify(f.expand())
display(f)
```

Output:

[![enter image description here][1]][1]


  [1]: https://i.stack.imgur.com/ZbgO0.png
