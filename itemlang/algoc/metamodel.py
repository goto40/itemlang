from __future__ import unicode_literals
from os.path import dirname, abspath
import itemlang.itemc.metamodel as item_metamodel
import itemlang.algoc.object_processors as object_processors

def get_meta_model(debug=False,**kwargs):
    this_folder = dirname(abspath(__file__))
    kwargs.update({
        "grammar_file_name": "../grammar/CustomAlgoLang.tx",
        "object_processors": {
            "Model": object_processors.check_model,
        },
    })
    mm = item_metamodel.get_meta_model(debug,**kwargs)

    return mm
