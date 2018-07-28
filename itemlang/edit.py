"""
simple editor for the model
WORK IN PROGRESS: 1%
"""

from __future__ import unicode_literals
import traceback
import itemlang.metamodel as custom_idl_metamodel
import codecs
import tkinter as tk
import sys
from textx.model import ObjCrossRef, ReferenceResolver
from textx import get_children_of_type
from textx.scoping import Postponed
import textx
import textx.scoping.tools as st
from arpeggio import Parser, Sequence, NoMatch, EOF, Terminal, NonTerminal
from textx.exceptions import TextXSyntaxError, TextXSemanticError
from textx.const import MULT_OPTIONAL, MULT_ONE, MULT_ONEORMORE, \
    MULT_ZEROORMORE, RULE_ABSTRACT, RULE_MATCH, MULT_ASSIGN_ERROR, \
    UNKNOWN_OBJ_ERROR


def all_terminals(pt,parent=None):
    for r in pt:
        if isinstance(r,Terminal):
            yield r,parent
        else:
            yield from all_terminals(r,r)

def edit(model_file):
    mm = custom_idl_metamodel.get_meta_model()
    model = mm.model_from_file(model_file)

    with codecs.open(model_file, 'r', encoding='utf-8') as f:
        model_str = f.read()

    # GUI setup
    fontname="Courier"
    root = tk.Tk()
    SV = tk.Scrollbar(root, orient=tk.VERTICAL)
    SH = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    T = tk.Text(root, height=4, width=50, wrap=tk.NONE)
    SV.pack(side=tk.RIGHT, fill=tk.Y)
    SH.pack(side=tk.BOTTOM, fill=tk.X)
    SV.config(command=T.yview)
    SH.config(command=T.xview)
    T.config(yscrollcommand=SV.set)
    T.config(xscrollcommand=SH.set)
    T.config(font=(fontname,12),foreground='black')
    T.insert(tk.END, model_str)
    T.pack(fill=tk.BOTH, expand=1)

    # first test: color some aspects
    print("----------")
    pt = model._tx_parser.parse_tree[0]
    r2pos1 = lambda o : model._tx_parser.pos_to_linecol(o.position-1)
    r2pos2 = lambda o : model._tx_parser.pos_to_linecol(o.position_end-1)
    for r ,p in all_terminals(pt):
        print("Terminal {}:{}:{}-{}.{}-{}.{}.".format(r,r.rule_name,r.name,
                                                      *r2pos1(r), *r2pos2(r)))
        tag='keyword'
        if p is not None and p.name.startswith('__asgn'):
            if (p.rule._attr_name=='name'):
                tag = 'name_value'
            else:
                tag = 'value'
        T.tag_add(tag,
                  '{}.{}'.format(*r2pos1(r)),
                  '{}.{}'.format(*r2pos2(r)))

    T.tag_config('keyword', foreground='black',
                 font=(fontname, 12, 'bold') )
    T.tag_config('value', foreground='blue',
                 font=(fontname, 12, 'normal') )
    T.tag_config('name_value', foreground='blue',
                 font=(fontname, 12, 'underline') )

    # run GUI
    tk.mainloop()