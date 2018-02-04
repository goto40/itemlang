from itemlang.itemc.metamodel import Struct, RawType
from textx import model_root

def path_to_file_name(struct):
    filename = ""
    return filename


def full_path_to_file_name(struct,function_name):
    filename = ""
    return filename + "{}.m".format(func_name(struct, function_name))

def func_name(struct,function_name):
    n=""
    if struct.parent.target_namespace:
        n = "_".join(struct.parent.target_namespace.name.split("."))+"_"
    return "{}_{}{}".format(function_name,n,struct.name)

def rawtype(t):
    if isinstance(t, Struct):
        return "struct"
    else:
        assert isinstance(t, RawType), "unexpected type found."
        if t.cpptype:
            cpptype = t.cpptype
            return cpptype.type
        else:
            if t.genericType=='signed':
                return "int{}".format(t.genericBits.bits)
            elif t.genericType == 'unsigned':
                return "uint{}".format(t.genericBits.bits)
            elif t.genericType == 'float':
                if t.genericBits.bits == 32:
                    return "single"
                elif t.genericBits.bits == 64:
                    return "double"
                else:
                    raise Exception("unexpected, unknown float with {} bits for ".format(t.genericBits.bits, t.name,
                                                                                          model_root(t)._tx_filename))
            else:
                raise Exception("unexpected, oct type specification is required for {} in file {}".format(t.name,
                                                                                                            model_root(t)._tx_filename))
