from __future__ import unicode_literals
import itemlang.algoc.metamodel as custom_algo_metamodel
from os import mkdir,makedirs
from shutil import copyfile
from os.path import dirname, join, exists, expanduser, abspath
import jinja2
from textx import children_of_type
import itemlang.algoc.support_cpp_code.custom_algo_cpptool as cpptool

def codegen(model_file=None, srcgen_folder=None, model_string=None, debug=False, generate_cpp=False, generate_python=False, generate_python_construct=False):

    this_folder = dirname(abspath(__file__))
    mm = custom_algo_metamodel.get_meta_model(
        generate_cpp=generate_cpp,
        generate_python=generate_python,
        generate_python_construct=generate_python_construct
    )

    # parse and validate

    if model_file and model_string:
        raise Exception("illegal call with model string AND model file specified.")
    elif not model_file and not model_string:
        raise Exception("illegal call with no model string or model file specified.")
    elif model_file:
        idl_model = mm.model_from_file(model_file)
    else: # model_string
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


def _generate_cpp_code(idl_model, srcgen_folder, this_folder):
    # attributes helper
    algos_folder = join(srcgen_folder , "algos")
    if not exists(algos_folder):
        makedirs(algos_folder)
    #copyfile(this_folder + "/support_cpp_code/target_lang/algo.h", algos_folder + "/attributes.h")
    #copyfile(this_folder + "/support_cpp_code/target_lang/tools.h", algos_folder + "/tools.h")

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder + "/support_cpp_code"),
        trim_blocks=True,
        lstrip_blocks=True)
    # Load Java template
    template = jinja_env.get_template('cpp_header.template')
    for algo in children_of_type("CppAlgo", idl_model):
        # For each entity generate java file
        struct_folder = join(srcgen_folder, cpptool.path_to_file_name(struct))
        if not exists(struct_folder):
            makedirs(struct_folder)
        with open(join(struct_folder,
                       "{}.h".format(struct.name)), 'w') as f:
            f.write(template.render(algo=algo,
                                    cpptool=cpptool
                                    ))


def _generate_python_code(idl_model, srcgen_folder, this_folder):
    pass
