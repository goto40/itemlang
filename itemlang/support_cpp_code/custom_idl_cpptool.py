from itemlang.metamodel import Struct, RawType
from textx import get_model


def open_namespace(namespace):
    res = ""
    for n in namespace.target_namespace.name.split("."):
        res += "namespace {} {{\n".format(n)
    return res


def close_namespace(namespace):
    res = ""
    for n in namespace.target_namespace.name.split("."):
        res += "}} // namespace {}\n".format(n)
    return res


def path_to_file_name(struct):
    filename = ""
    if struct.parent.target_namespace:
        filename = "/".join(struct.parent.target_namespace.name.split("."))
    return filename


def full_path_to_file_name(struct):
    filename = ""
    if struct.parent.target_namespace:
        filename = "/".join(struct.parent.target_namespace.name.split("."))
    return filename + "/" + struct.name + ".h"


def has_include(t):
    if isinstance(t, Struct):
        return True
    else:
        assert isinstance(t, RawType), "unexpected type found."
        if t.cpptype:
            return t.cpptype.including != None
        else:
            if t.genericType == 'signed':
                return True
            elif t.genericType == 'unsigned':
                return True
        return False


def get_include(t):
    if isinstance(t, Struct):
        return full_path_to_file_name(t)
    else:
        assert isinstance(t, RawType), "unexpected type found."
        if t.cpptype:
            assert t.cpptype, "unexpected hasInclude/getInclude combination."
            return t.cpptype.including
        else:
            if t.genericType == 'signed':
                return "<cstdint>"
            elif t.genericType == 'unsigned':
                return "<cstdint>"


def fqn(t):
    if isinstance(t, Struct):
        struct = t
        fqn_result = ""
        if struct.parent.target_namespace:
            fqn_result = "::".join(struct.parent.target_namespace.name.split("."))
        return fqn_result + "::" + struct.name
    else:
        assert isinstance(t, RawType), "unexpected type found."
        if t.cpptype:
            cpptype = t.cpptype
            return cpptype.type
        else:
            if t.genericType == 'signed':
                return "int{}_t".format(t.genericBits.bits)
            elif t.genericType == 'unsigned':
                return "uint{}_t".format(t.genericBits.bits)
            elif t.genericType == 'float':
                if t.genericBits.bits == 32:
                    return "float"
                elif t.genericBits.bits == 64:
                    return "double"
                elif t.genericBits.bits == 128:
                    return "long double"
                else:
                    raise Exception("unexpected, unknown float with {} bits for ".format(
                        t.genericBits.bits,
                        t.name,
                        get_model(t)._tx_filename))
            else:
                raise Exception("unexpected, C++ type specification is required for {} in file {}".format(
                    t.name,
                    get_model(t)._tx_filename))


def default_value_init_code(attribute, force=False):
    if attribute.default_value:
        return " = {}".format(attribute.default_value)
    else:
        if force:
            raise Exception("expected default value for attribute {}".format(attribute.name))
        else:
            return ""
