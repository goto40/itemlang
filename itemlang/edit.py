"""
simple editor for the model
"""

from __future__ import unicode_literals
import itemlang.metamodel as custom_idl_metamodel
import codecs
import tkinter as tk
import textx
import textx.scoping.tools as st

def edit(model_file):
    mm = custom_idl_metamodel.get_meta_model()
    #model = mm.model_from_file(model_file)

    with codecs.open(model_file, 'r', encoding='utf-8') as f:
        model_str = f.read()

    parser = mm._parser.clone()
    parser.parse(model_str, file_name = model_file)

    # GUI setup
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
    T.insert(tk.END, model_str)
    T.pack(fill=tk.BOTH, expand=1)

    # first test: color some aspects
    print("----------")

    # run GUI
    tk.mainloop()