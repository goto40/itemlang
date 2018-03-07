from __future__ import unicode_literals
from os.path import dirname, abspath
from textx import metamodel_from_file, get_children_of_type
import os
import textx.scoping.providers as scoping_providers
import textx.scoping.tools as scoping_tools
from functools import reduce
import itemlang.itemc.object_processors as object_processors


class CustomIdlBase(object):
    def __init__(self):
        pass

    def _init_xtextobj(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class RawType(CustomIdlBase):
    def __init__(self, **kwargs):
        super(RawType, self).__init__()
        self._init_xtextobj(**kwargs)


class Struct(CustomIdlBase):
    def __init__(self, **kwargs):
        super(Struct, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_arrays_with_adjustable_dimensions(self):
        result = []
        for a in filter(lambda x: type(x) is ArrayAttribute, self.attributes):
            if not a.has_fixed_size():
                result.append(a)
        return result

    def get_attributes_which_affects_size(self):
        result = []
        for a in filter(lambda x: type(x) is ScalarAttribute, self.attributes):
            if a.affects_size():
                result.append(a)
        return result

    def has_adjustable_array_dimensions(self):
        return len(self.get_arrays_with_adjustable_dimensions()) > 0

    def get_structs_of_attributes(self):
        result = set()
        for s in filter(lambda x: type(x) is Struct, map(lambda x: x.type, self.attributes)):
            result.add(s)
        return result

    def get_raw_types_of_attributes(self):
        result = set()
        for s in filter(lambda x: type(x) is RawType, map(lambda x: x.type, self.attributes)):
            result.add(s)
        return result


class ScalarAttribute(CustomIdlBase):
    def __init__(self, **kwargs):
        super(ScalarAttribute, self).__init__()
        self._init_xtextobj(**kwargs)

    def affects_size(self):
        struct = scoping_tools.get_recursive_parent_with_typename(self, "Struct")
        for a in filter(lambda x: type(x) is ArrayAttribute, struct.attributes):
            for d in a.array_dimensions:
                for ref in get_children_of_type("ScalarRef", d.array_size):
                    if self is ref.ref0:
                        return True
        return False

    def has_raw_type(self):
        return type(self.type) is RawType


class ArrayAttribute(CustomIdlBase):
    def __init__(self, **kwargs):
        super(ArrayAttribute, self).__init__()
        self._init_xtextobj(**kwargs)

    def has_fixed_size(self):
        return reduce(lambda x, y: x and y, map(lambda x: x.array_size.has_fixed_size(), self.array_dimensions), True)

    def has_raw_type(self):
        return type(self.type) is RawType


class ArrayDimension(CustomIdlBase):
    def __init__(self, **kwargs):
        super(ArrayDimension, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_array_index_name(self):
        if self.array_index_name:
            return self.array_index_name
        else:
            return "index"


def get_meta_model(debug=False, **kwargs):
    from itemlang.itemc.metamodel_formula import Sum, Mul, Dif, Div, Val, ScalarRef

    grammar_file_name = '../grammar/CustomIDL.tx'

    my_providers = {
        "*.*": scoping_providers.FQNImportURI(),
        "ScalarRef.ref0": scoping_providers.RelativeName("parent(Struct).attributes"),
        "ScalarRef.ref1": scoping_providers.RelativeName("ref0.type.attributes"),
        "ScalarRef.ref2": scoping_providers.RelativeName("ref1.type.attributes"),
    }

    my_object_processors = {
        "ScalarRef": object_processors.check_scalar_ref,
        "Struct": object_processors.CheckRawTypes(kwargs),
        "ArrayDimension": object_processors.check_array_dimensions,
        "ArrayAttribute": object_processors.check_array_attribute,
        "RawType": object_processors.check_raw_type_has_defined_bits
    }

    this_folder = dirname(abspath(__file__))
    mm = metamodel_from_file(os.path.join(this_folder, grammar_file_name), debug=debug,
                             classes=[Sum, Mul, Dif, Div, Val, ScalarRef, RawType, Struct, ArrayAttribute,
                                      ScalarAttribute, ArrayDimension])

    mm.register_scope_providers(my_providers)
    mm.register_obj_processors(my_object_processors)

    return mm
