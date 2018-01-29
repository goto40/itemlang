from __future__ import unicode_literals
from os.path import dirname, abspath
import itemlang.itemc.metamodel as item_metamodel
import itemlang.algoc.object_processors as object_processors

class CustomAlgoBase(object):
    def __init__(self):
        pass

    def _init_xtextobj(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class Algo(CustomAlgoBase):
    def __init__(self, **kwargs):
        super(Algo, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_all_structs_of_arguments(self):
        s = set()
        for a in self.arguments:
            #print("add {}:{}".format(a.name, a.type.name))
            s.add(a.type)
        return list(s)


def get_meta_model(debug=False,**kwargs):
    this_folder = dirname(abspath(__file__))
    kwargs.update({
        "grammar_file_name": "../grammar/CustomAlgoLang.tx",
        "classes": [Algo],
        "object_processors": {
            "Model": object_processors.check_model,
        },
    })
    mm = item_metamodel.get_meta_model(debug,**kwargs)

    return mm
