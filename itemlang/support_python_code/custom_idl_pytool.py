from textx import get_model


def path_to_file_name(struct):
    filename = ""
    if struct.parent.target_namespace:
        filename = "/".join(struct.parent.target_namespace.name.split("."))
    return filename


def full_path_to_file_name(struct):
    filename = ""
    if struct.parent.target_namespace:
        filename = "/".join(struct.parent.target_namespace.name.split("."))
    return filename + "/" + struct.name + ".py"


def has_import(thetype):
    if thetype.pythontype:
        return len(thetype.pythontype.fromlib) > 0
    else:
        return True


def get_import(thetype):
    if thetype.pythontype:
        return thetype.pythontype.fromlib
    else:
        return "numpy"


def the_package(struct):
    if struct.parent.target_namespace:
        return struct.parent.target_namespace.name + "." + struct.name
    else:
        return struct.name


def typename(thetype):
    from itemlang.metamodel import RawType
    if type(thetype) is RawType:
        if thetype.pythontype:
            if thetype.pythontype.fromlib:
                res = thetype.pythontype.fromlib + "." + thetype.pythontype.type
                # print("typename (rawtype) with lib: {}".format(res))
                return res
            else:
                res = thetype.pythontype.type
                # print("typename (rawtype) w/o lib: {}".format(res))
                return res
        else:
            if thetype.genericType == 'signed':
                return "numpy.int{}".format(thetype.genericBits.bits)
            elif thetype.genericType == 'unsigned':
                return "numpy.uint{}".format(thetype.genericBits.bits)
            elif thetype.genericType == 'float':
                return "numpy.float{}".format(thetype.genericBits.bits)
            else:
                raise Exception(
                    "unexpected, python type specification is required for {} in file {}".format(
                        thetype.name,
                        get_model(thetype)._tx_filename))
    else:
        res = the_package(thetype) + "." + thetype.name
        # print("typename (struct): {}".format(res))
        return res


def format(thetype):
    if thetype.pythontype:
        return thetype.pythontype.format
    else:
        if thetype.genericType == 'signed':
            if thetype.genericBits.bits == 8:
                return "b"
            elif thetype.genericBits.bits == 16:
                return "h"
            elif thetype.genericBits.bits == 32:
                return "l"
            elif thetype.genericBits.bits == 64:
                return "q"
            else:
                raise Exception(
                    "unexpected, python type specification is required for {} in file {}".format(
                        thetype.name,
                        get_model(thetype)._tx_filename))
        elif thetype.genericType == 'unsigned':
            if thetype.genericBits.bits == 8:
                return "B"
            elif thetype.genericBits.bits == 16:
                return "H"
            elif thetype.genericBits.bits == 32:
                return "L"
            elif thetype.genericBits.bits == 64:
                return "Q"
            else:
                raise Exception(
                    "unexpected, python type specification is required for {} in file {}".format(
                        thetype.name,
                        get_model(thetype)._tx_filename))
        elif thetype.genericType == 'float':
            if thetype.genericBits.bits == 32:
                return "f"
            elif thetype.genericBits.bits == 64:
                return "d"
            else:
                raise Exception(
                    "unexpected, python type specification is required for {} in file {}".format(
                        thetype.name,
                        get_model(thetype)._tx_filename))
        else:
            raise Exception("unexpected, python type specification is required for {} in file {}".format(
                thetype.name,
                get_model(thetype)._tx_filename))


def get_meta_info(attribute):
    from itemlang.metamodel import RawType
    thetype = attribute.type
    if type(thetype) is RawType:
        return {"model_type_name": thetype.name, "format": format(thetype)}
    else:
        return {"model_type_name": thetype.name}


def default_value_init_code(attribute, fixed_read_only=False):
    from itemlang.metamodel import Struct
    if attribute.default_value and not (type(attribute.type) is Struct):
        return "{}".format(attribute.default_value)
    else:
        if type(attribute.type) is Struct:
            if fixed_read_only:
                return "{}(True)".format(typename(attribute.type))
            else:
                return "{}(read_only)".format(typename(attribute.type))
        else:
            return "{}()".format(typename(attribute.type))
