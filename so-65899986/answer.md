Mathjax itself doesn't have the `table`/`tabular` environment, but still it's possible to use the `array` environment for this ([link1](https://math.meta.stackexchange.com/a/6737/68328) ; [link2](https://math.meta.stackexchange.com/a/22213/68328) ; [link3](https://help.geogebra.org/topic/-resolved-mostly-latex-assistance-mathjax-coding?lang=ca)).

So based on this, I wrote the following formatting function called `fmt_table` which formats the formulas like you mentioned:


```python3
from sympy import Ynm, simplify, symbols, latex
theta, phi = symbols('\Theta \phi')
from IPython.display import HTML, display, Math, Latex

def fmt_table(data,center_data=False,add_row_nums=False):
    from math import ceil
    buf='''
\\newcommand\\T{\\Rule{0pt}{1em}{.3em}}
\\begin{array}{%s}    
'''
    max_cols = max(len(r) for r in data)
    column_spec = '|' + '|'.join(['c']*max_cols) + '|'
    buf = buf % column_spec
    row_idx = 0
    for row_data in data:
        row = ''
        if add_row_nums and row_idx > 0:
            row += str(row_idx) + " & "
        if center_data and row_idx > 0:
            to_add = ceil( (max_cols - len(row_data))/2 )
            row += ' & '.join([''] * to_add)
        row += ' & '.join(row_data)
        if row_idx == 0:
            row = '''\\hline''' + row + '''\\\\\hline'''
        else:
            row += '''\\\\\hline'''
        row += "\n"
        buf +=row
        row_idx += 1
    buf += '''\\end{array}'''
    # print(buf)
    return buf
    

tbl = []
tbl.append(['\\texttt{m/l}','-2','-1','0','1','2'])
for l in range (0, 3):
    new_row = []    
    for m in range(-l, l+1):
        h = simplify(Ynm(l, m, theta, phi).expand(func=True))
        new_row.append(latex(h))
    tbl.append(new_row)
    

display(Math(fmt_table(tbl,add_row_nums=True,center_data=True)))
```

OUTPUT:

[![enter image description here][1]][1]

All the code in this answer is [also available here](https://github.com/wsdookadr/so/tree/master/so-65899986).

  [1]: https://i.stack.imgur.com/QGBhi.png
