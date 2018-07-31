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


def all_terminals(pt,parent=None, parent_list=None):
    if parent_list is None: parent_list=[]
    for r in pt:
        if isinstance(r,Terminal):
            yield r,parent, parent_list
        else:
            yield from all_terminals(r,r,[r]+parent_list)

def all_model_elements(model_obj,metamodel=None,current_metaattr=None):
    """
    Depth-first model object processing.
    """
    if metamodel is None:
        metamodel = model_obj._tx_metamodel
    many = [MULT_ONEORMORE, MULT_ZEROORMORE]

    # enter recursive visit of attributes only, if the class of the
    # object being processed is a meta class of the current meta model
    if model_obj.__class__.__name__ in metamodel:
        yield model_obj, current_metaattr
        current_metaclass_of_obj = metamodel[model_obj.__class__.__name__]
        for metaattr in current_metaclass_of_obj._tx_attrs.values():
            # If attribute is base type or containment reference go down
            if metaattr.cont:
                attr = getattr(model_obj, metaattr.name)
                if attr:
                    if metaattr.mult in many:
                        for _, obj in enumerate(attr):
                            if obj:
                                yield from all_model_elements(obj, metamodel, metaattr)
                    else:
                        yield from all_model_elements(attr, metamodel, metaattr)
            else:
                attr = getattr(model_obj, metaattr.name)
                if attr:
                    if metaattr.mult in many:
                        for _, obj in enumerate(attr):
                            if obj:
                                yield obj, metaattr
                    else:
                        yield attr, metaattr



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
    T = tk.Text(root, height=25, width=80, wrap=tk.NONE)
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

    for r ,p, pl in all_terminals(pt):
        print("Terminal {}:{}:{}-{}.{}-{}.{}.".format(r,r.rule_name,r.name,
                                                      *r2pos1(r), *r2pos2(r)))
        tag='keyword'
        # TODO analyze pl stack --> find outer element with same posK
        if p is not None and p.name.startswith('__asgn'):
            if (p.rule._attr_name=='name'):
                tag = 'name_value'
            else:
                tag = 'value'
            # how to identify links?
            # maybe I need to decorate the parse tree with links to the model?
            # or the meta model?
        T.tag_add(tag,
                  '{}.{}'.format(*r2pos1(r)),
                  '{}.{}'.format(*r2pos2(r)))

    T.tag_config('keyword', foreground='black',
                 font=(fontname, 12, 'bold') )
    T.tag_config('value', foreground='green',
                 font=(fontname, 12, 'normal') )
    T.tag_config('link', foreground='blue',
                 font=(fontname, 12, 'normal'))
    T.tag_config('name_value', foreground='magenta',
                 font=(fontname, 12, 'normal') )

    # run GUI
    tk.mainloop()