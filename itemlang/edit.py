"""
simple editor for the model
WORK IN PROGRESS: 1%
"""

from __future__ import unicode_literals
import itemlang.metamodel as custom_idl_metamodel
import codecs
import tkinter as tk
from arpeggio import Parser, Sequence, NoMatch, EOF, Terminal, NonTerminal


def all_terminals_and_links(pt,parent=None, parent_list=None):
    if parent_list is None: parent_list=[]
    for r in pt:
        if isinstance(r,Terminal):
            yield r,parent, parent_list, False
        else:
            # parent.rule/_tx_class/_tx_attrs/<name>/cont==False & ref=True
            # later: rule/_attr_name=<name>
            if parent is not None and hasattr(r.rule, "_attr_name"):
                name = r.rule._attr_name
                metaattr = parent.rule._tx_class._tx_attrs[name]
                if metaattr.ref and not metaattr.cont:
                    yield r, parent, parent_list, True
                    return
            yield from all_terminals_and_links(r,r,[r]+parent_list)


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

    for r ,p, pl, islink in all_terminals_and_links(pt):
        #print("Terminal {}:{}:{}-{}.{}-{}.{}.".format(r,r.rule_name,r.name,
        #                                              *r2pos1(r), *r2pos2(r)))
        tag='keyword'
        # TODO analyze pl stack --> find outer element with same posK
        if islink:
            tag = 'link'
        elif p is not None and p.name.startswith('__asgn'):
            if (p.rule._attr_name=='name'):
                tag = 'name_value'
            else:
                tag = 'value'
        T.tag_add(tag,
                  '{}.{}'.format(*r2pos1(r)),
                  '{}.{}'.format(*r2pos2(r)))


    T.tag_config('keyword', foreground='black',
                 font=(fontname, 12, 'bold') )
    T.tag_config('value', foreground='green',
                 font=(fontname, 12, 'normal') )
    T.tag_config('link', foreground='blue',
                 font=(fontname, 12, 'bold'))
    T.tag_config('name_value', foreground='magenta',
                 font=(fontname, 12, 'normal') )

    # run GUI
    tk.mainloop()
