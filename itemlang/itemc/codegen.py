"""
An example how to generate c++ code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""

from __future__ import unicode_literals
import itemlang.itemc.metamodel as custom_idl_metamodel
from os import mkdir, makedirs
from shutil import copyfile
from os.path import dirname, join, exists, abspath
import jinja2
from textx import get_children_of_type


def codegen(model_file=None, srcgen_folder=None, model_string=None, debug=False, generate_cpp=False,
            generate_python=False, generate_python_construct=False, generate_octave=False):
    this_folder = dirname(abspath(__file__))
    mm = custom_idl_metamodel.get_meta_model(
        generate_cpp=generate_cpp,
        generate_python=generate_python,
        generate_python_construct=generate_python_construct,
        generate_octave=generate_octave
    )

    # parse and validate

    if model_file and model_string:
        raise Exception("illegal call with model string AND model file specified.")
    elif not model_file and not model_string:
        raise Exception("illegal call with no model string or model file specified.")
    elif model_file:
        idl_model = mm.model_from_file(model_file)
    else:  # model_string
        idl_model = mm.model_from_str(model_string)

    # generate ocde
    if not srcgen_folder:
        srcgen_folder = join(this_folder, 'srcgen')
        if not exists(srcgen_folder):
            mkdir(srcgen_folder)
    print("generating into {}".format(srcgen_folder))

    if generate_cpp:
        _generate_cpp_code(idl_model, srcgen_folder, this_folder)
    if generate_python:
        _generate_python_code(idl_model, srcgen_folder, this_folder)
    if generate_python_construct:
        _generate_python_construct_code(idl_model, srcgen_folder, this_folder)
    if generate_octave:
        _generate_octave_code(idl_model, srcgen_folder, this_folder)


def _generate_cpp_code(idl_model, srcgen_folder, this_folder):
    import itemlang.itemc.support_cpp_code.custom_idl_cpptool as cpptool
    # attributes helper
    attributes_folder = join(srcgen_folder, "attributes")
    if not exists(attributes_folder):
        makedirs(attributes_folder)
    copyfile(this_folder + "/support_cpp_code/target_lang/attributes.h", attributes_folder + "/attributes.h")
    copyfile(this_folder + "/support_cpp_code/target_lang/tools.h", attributes_folder + "/tools.h")
    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder + "/support_cpp_code"),
        trim_blocks=True,
        lstrip_blocks=True)
    # Load Java template
    template = jinja_env.get_template('cpp_header.template')
    for struct in get_children_of_type("Struct", idl_model):
        # For each entity generate java file
        struct_folder = join(srcgen_folder, cpptool.path_to_file_name(struct))
        if not exists(struct_folder):
            makedirs(struct_folder)
        with open(join(struct_folder,
                       "{}.h".format(struct.name)), 'w') as f:
            f.write(template.render(struct=struct,
                                    cpptool=cpptool
                                    ))


def _generate_python_code(idl_model, srcgen_folder, this_folder):
    import itemlang.itemc.support_python_code.custom_idl_pytool as pytool
    # attributes helper
    attributes_folder = join(srcgen_folder, "attributes")
    if not exists(attributes_folder):
        makedirs(attributes_folder)
    copyfile(this_folder + "/support_python_code/target_lang/attributes.py", attributes_folder + "/attributes.py")
    copyfile(this_folder + "/support_python_code/target_lang/tools.py", attributes_folder + "/tools.py")
    with open(attributes_folder + "/__init__.py", 'w') as f:
        f.write("")
    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder + "/support_python_code"),
        trim_blocks=True,
        lstrip_blocks=True)
    # Load Java template
    template = jinja_env.get_template('python.template')
    for struct in get_children_of_type("Struct", idl_model):
        # For each entity generate java file
        struct_folder = join(srcgen_folder, pytool.path_to_file_name(struct))
        if not exists(struct_folder):
            makedirs(struct_folder)

        if struct.parent.target_namespace:
            parts = struct.parent.target_namespace.name.split(".")
            dir = srcgen_folder
            for part in parts:
                dir = join(dir, part)
                init_filename = join(dir, "__init__.py")
                with open(init_filename, 'w') as f:
                    f.write("")

        with open(join(struct_folder,
                       "{}.py".format(struct.name)), 'w') as f:
            f.write(template.render(struct=struct,
                                    pytool=pytool
                                    ))


def _generate_python_construct_code(idl_model, srcgen_folder, this_folder):
    import itemlang.itemc.support_python_construct_code.custom_idl_pyctool as pyctool
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder + "/support_python_construct_code"),
        trim_blocks=True,
        lstrip_blocks=True)
    # Load Java template
    template = jinja_env.get_template('python-construct.template')
    for struct in get_children_of_type("Struct", idl_model):
        # For each entity generate java file
        struct_folder = join(srcgen_folder, pyctool.path_to_file_name(struct))
        if not exists(struct_folder):
            makedirs(struct_folder)

        if struct.parent.target_namespace:
            parts = struct.parent.target_namespace.name.split(".")
            dir = srcgen_folder
            for part in parts:
                dir = join(dir, part)
                init_filename = join(dir, "__init__.py")
                with open(init_filename, 'w') as f:
                    f.write("")

        with open(join(srcgen_folder, pyctool.full_path_to_file_name(struct)), 'w') as f:
            f.write(template.render(struct=struct,
                                    pyctool=pyctool
                                    ))


def _generate_octave_code(idl_model, srcgen_folder, this_folder):
    import itemlang.itemc.support_octave_code.custom_idl_octtool as octtool
    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder + "/support_octave_code"),
        trim_blocks=True,
        lstrip_blocks=True)
    # Load Java template
    for func_name in ["read", "write", "create", "check"]:
        template = jinja_env.get_template('octave_{}.template'.format(func_name))
        for struct in get_children_of_type("Struct", idl_model):
            struct_folder = join(srcgen_folder, octtool.path_to_file_name(struct))
            if not exists(struct_folder):
                makedirs(struct_folder)
            with open(join(srcgen_folder, octtool.full_path_to_file_name(struct, func_name)), 'w') as f:
                f.write(template.render(struct=struct,
                                        octtool=octtool
                                        ))
