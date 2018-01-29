from __future__ import unicode_literals
from os.path import dirname, abspath
import itemlang.itemc.metamodel as item_metamodel
from textx import metamodel_from_file
import os
import textx.scoping as scoping

def get_meta_model(debug=False,**kwargs):
    this_folder = dirname(abspath(__file__))
    kwargs.update({
        "grammar_file_name": "../grammar/CustomAlgoLang.tx"
    })
    mm = item_metamodel.get_meta_model(debug,**kwargs)

    return mm
