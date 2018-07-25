from os.path import expanduser
from itemlang.codegen import codegen
from itemlang.edit import edit


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
    parser.add_argument('--generate-octave', dest='generate_octave', default=False,
                        action='store_true', help='generate octave code')
    parser.add_argument('-edit', dest='edit', default=False,
                        action='store_true', help='edit model')

    args = parser.parse_args()
    for model_file in args.model_files:
        if args.edit:
            edit(model_file=model_file)
        else:
            codegen(model_file=model_file,
                         srcgen_folder=expanduser(args.srcgen),
                         generate_cpp=args.generate_cpp,
                         generate_python=args.generate_python,
                         generate_octave=args.generate_octave
                         )

