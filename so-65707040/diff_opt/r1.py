import hunter
import sys
from hunter import Q, When, Stop, Action
from hunter.actions import  ColorStreamAction

formula_ltx = r'''
\documentclass[border=2pt,varwidth]{letter}
\usepackage{amsmath}
\pagenumbering{gobble}
\begin{document}
\[ \texttt{TITLE} \]
\[ FORMULA \]
\end{document}
'''

# ==============
# == Tracing ===
# ==============

from sympy.printing.latex import LatexPrinter, print_latex, latex

global call_tree_root

# a node object to hold an observed function call
# with its argument, its return value and its function name
class Node(object):
    def __init__(self, arg=None, retval=None, func_name=None):
        self.arg = arg
        self.retval = retval
        self.arg_ascii = ""
        self.retval_ascii = ""
        self.func_name = func_name
        self.uid = 0
        self.children = []

# this is a hunter action where we build a call graph and populate it
# so we can later render it
#
# CGBAction (Call Graph Builder Action)
class CGBAction(ColorStreamAction):
    def __init__(self, *args, **kwargs):
        super(ColorStreamAction, self).__init__(*args, **kwargs)
        # a custom call stack
        self.tstack = []
        global call_tree_root
        call_tree_root = Node(arg="",func_name="root")
        self.node_idx = 1
        self.tstack.append(call_tree_root)

    def __call__(self, event):
        if event.kind in ['return','call']:
            if event.kind == 'return':
                print(str(event.arg))
                if len(self.tstack) > 0:
                    top = self.tstack.pop()
                    top.retval = latex(event.arg)
                    top.retval_ascii = str(event.arg)

            elif event.kind == 'call':
                print(str(event.locals.get('self')))
                new = Node()
                new.uid = self.node_idx
                new.arg = latex(event.locals.get('self'))
                new.arg_ascii = str(event.locals.get('self'))
                top = self.tstack[-1]
                self.tstack.append(new)
                top.children.append(new)
                new.func_name = event.module + ":" + event.function
                self.node_idx += 1

hunter.trace(
        Q(module_contains="sympy",function_in=['_eval_derivative','diff','_eval_derivative_n_times'],kind_in=["call","return"],action=CGBAction),
        )

from sympy import *
x = symbols('x')
u = Function('u')(x)
v = Function('v')(x)
f = u * v
f.diff(x,5)

# ============================
# == Call graph rendering ====
# ============================

import os
import re
OUT_DIR="formulas"

if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

def write_formula(prefix,uid,formula,title):
    TEX = uid + prefix + ".tex"
    PDF = uid + prefix + ".pdf"
    PNG = uid + prefix + ".png"

    TEX_PATH = OUT_DIR + "/" + TEX
    with open(TEX_PATH,"w") as f:
        ll = formula_ltx
        ll = ll.replace("FORMULA",formula)
        ll = ll.replace("TITLE",title)
        f.write(ll)

    # compile formula
    CMD = """
        cd formulas ; 
        pdflatex {TEX} ;
        convert -trim -density 300 {PDF} -quality 90 -colorspace RGB {PNG} ;
    """.format(TEX=TEX,PDF=PDF,PNG=PNG)

    os.system(CMD)

buf_nodes = ""
buf_edges = ""
def dfs_tree(x):
    global buf_nodes, buf_edges

    arg = ("" if x.arg is None else x.arg)
    rv  = ("" if x.retval is None else x.retval)
    arg = arg.replace("\r","")
    rv = rv.replace("\r","")

    formula = arg + "\\Rightarrow " + rv
    print(x.func_name + " -> " + x.arg_ascii + " -> " + x.retval_ascii)

    x.func_name = x.func_name.replace("_","\\_")
    write_formula("",str(x.uid),formula,x.func_name)

    buf_nodes += """
    {0} [image="{0}.png" label=""];
    """.format(x.uid);

    for y in x.children:
        buf_edges += "{0} -> {1};\n".format(x.uid,y.uid);
        dfs_tree(y)

dfs_tree(call_tree_root)

g = open(OUT_DIR + "/graph.dot", "w")
g.write("digraph g{")
g.write(buf_nodes)
g.write(buf_edges)
g.write("}\n")
g.close()
os.system("""cd formulas ; dot -Tpng graph.dot > graph.png ;""")

