"""
simple editor for the model
WORK IN PROGRESS: 1%
"""

from __future__ import unicode_literals
import itemlang.metamodel as custom_idl_metamodel
import codecs
import tkinter as tk
from arpeggio import Parser, Sequence, NoMatch, EOF, Terminal, NonTerminal


def all_terminals_and_links(pt, parent=None, parent_list=None):
    if parent_list is None: parent_list = []
    for r in pt:
        if isinstance(r, Terminal):
            yield r, parent, parent_list, False
        else:
            # parent.rule/_tx_class/_tx_attrs/<name>/cont==False & ref=True
            # later: rule/_attr_name=<name>
            if parent is not None and hasattr(r.rule, "_attr_name"):
                name = r.rule._attr_name
                metaattr = parent.rule._tx_class._tx_attrs[name]
                if metaattr.ref and not metaattr.cont:
                    yield r, parent, parent_list, True
                    return
            yield from all_terminals_and_links(r, r, [r] + parent_list)

def edit(model_filename):
    mm = custom_idl_metamodel.get_meta_model()
    e=Editor(mm)
    e.edit(model_filename)


# from https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
# create a proxy for the underlying widget
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)
        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")
        return result

class Editor:
    def __init__(self, mm):
        self.mm = mm
        # GUI setup
        self.fontname="Courier"
        self.root = tk.Tk()
        SV = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        SH = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.T = CustomText(self.root, height=25, width=80, wrap=tk.NONE)
        SV.pack(side=tk.RIGHT, fill=tk.Y)
        SH.pack(side=tk.BOTTOM, fill=tk.X)
        SV.config(command=self.T.yview)
        SH.config(command=self.T.xview)
        self.T.config(yscrollcommand=SV.set)
        self.T.config(xscrollcommand=SH.set)
        self.T.config(font=(self.fontname,12),foreground='black')
        self.T.pack(fill=tk.BOTH, expand=1)
        self.T.bind("<<TextModified>>", self.onModification)

    def onModification(self, event=None):
        print("modified!")

    def analyze_and_set_tags(self, model_text, file_name):

        for tag in self.T.tag_names():
            self.T.tag_delete(tag)

        #model = self.mm.model_from_str(model_text)
        model = self.mm.model_from_file(file_name)
        # first test: color some aspects
        pt = model._tx_parser.parse_tree[0]
        r2pos1 = lambda o : model._tx_parser.pos_to_linecol(o.position-1)
        r2pos2 = lambda o : model._tx_parser.pos_to_linecol(o.position_end-1)

        for r ,p, pl, islink in all_terminals_and_links(pt):
            #print("Terminal/Link({}) {}:{}:{}-{}.{}-{}.{}.".format(islink,r,
            #                      r.rule_name,r.name,*r2pos1(r), *r2pos2(r)))
            tag='keyword'
            if islink:
                tag = 'link'
            elif p is not None and p.name.startswith('__asgn'):
                if (p.rule._attr_name=='name'):
                    tag = 'name_value'
                else:
                    tag = 'value'
            self.T.tag_add(tag,
                      '{}.{}'.format(*r2pos1(r)),
                      '{}.{}'.format(*r2pos2(r)))

        self.T.tag_config('keyword', foreground='black',
                     font=(self.fontname, 12, 'bold') )
        self.T.tag_config('value', foreground='green',
                     font=(self.fontname, 12, 'normal') )
        self.T.tag_config('link', foreground='blue',
                     font=(self.fontname, 12, 'bold'))
        self.T.tag_config('name_value', foreground='magenta',
                     font=(self.fontname, 12, 'normal') )

    def edit(self, model_filename):
        with codecs.open(model_filename, 'r', encoding='utf-8') as f:
            model_str = f.read()

        self.T.insert(tk.END, model_str)

        self.analyze_and_set_tags(model_str, model_filename)


        # run GUI
        tk.mainloop()
