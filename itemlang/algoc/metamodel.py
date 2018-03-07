from __future__ import unicode_literals
from os.path import dirname, abspath, join
from textx import metamodel_from_file
import textx.scoping.providers as scoping_providers
import textx.scoping as scoping


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
    grammar_file_name = '../grammar/CustomAlgoLang.tx'

    my_providers = {
        "*.*": scoping_providers.FQNImportURI(),
    }

    my_object_processors = {
    }

    this_folder = dirname(abspath(__file__))

    mm = metamodel_from_file( join(this_folder,grammar_file_name), debug=debug,
                              classes=[Algo])
    mm.register_scope_providers(my_providers)
    mm.register_obj_processors(my_object_processors)

    if not scoping.MetaModelProvider.knows("*.item"):
        import itemlang.itemc.metamodel as imetamodel
        imm = imetamodel.get_meta_model(debug, **kwargs)
        scoping.MetaModelProvider.add_metamodel("*.item", imm)
        scoping.MetaModelProvider.add_metamodel("*.inc", imm)

    return mm
