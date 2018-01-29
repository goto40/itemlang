from os.path import expanduser
from itemlang.itemc.codegen import codegen as item_codegen
from itemlang.algoc.codegen import codegen as algo_codegen

def itemc():
    import argparse
    parser = argparse.ArgumentParser(description='generate code for the item model.')
    parser.add_argument('model_files', metavar='model_files', type=str, nargs='+',
                        help='model filenames')
    parser.add_argument('--src-gen-folder', dest='srcgen', default="src-gen", type=str,
                        help='folder where to generate the code')
    parser.add_argument('--generate-cpp', dest='generate_cpp', default=False,
                        action='store_true', help='generate C++ code')
    parser.add_argument('--generate-python', dest='generate_python', default=False,
                        action='store_true', help='generate python code')
    parser.add_argument('--generate-python-construct', dest='generate_python_construct', default=False,
                        action='store_true', help='generate python code (construct based)')

    args = parser.parse_args()
    for model_file in args.model_files:
        item_codegen(model_file=model_file, srcgen_folder=expanduser(args.srcgen),
                generate_cpp=args.generate_cpp,
                generate_python=args.generate_python,
                generate_python_construct=args.generate_python_construct)

def algoc():
    import argparse
    parser = argparse.ArgumentParser(description='generate code for the algo model.')
    parser.add_argument('model_files', metavar='model_files', type=str, nargs='+',
                        help='model filenames')
    parser.add_argument('--src-gen-folder', dest='srcgen', default="src-gen", type=str,
                        help='folder where to generate the code')
    parser.add_argument('--generate-cpp', dest='generate_cpp', default=False,
                        action='store_true', help='generate C++ code')
    parser.add_argument('--generate-python', dest='generate_python', default=False,
                        action='store_true', help='generate python code')

    args = parser.parse_args()
    for model_file in args.model_files:
        algo_codegen(model_file=model_file, srcgen_folder=expanduser(args.srcgen),
                generate_cpp=args.generate_cpp,
                generate_python=args.generate_python)

