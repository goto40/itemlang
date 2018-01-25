if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='generate code for the custom idl model.')
    parser.add_argument('model_file', metavar='model_file', type=str,
                        help='model filename')
    parser.add_argument('--src-gen-folder', dest='srcgen', default="srcgen", type=str,
                        help='folder where to generate the code')
    parser.add_argument('--generate-cpp', dest='generate_cpp', default=False,
                        action='store_true', help='generate C++ code')
    parser.add_argument('--generate-python', dest='generate_python', default=False,
                        action='store_true', help='generate python code')
    parser.add_argument('--generate-python-construct', dest='generate_python_construct', default=False,
                        action='store_true', help='generate python code (construct based)')

    args = parser.parse_args()
    codegen(model_file=args.model_file, srcgen_folder=expanduser(args.srcgen),
            generate_cpp=args.generate_cpp,
            generate_python=args.generate_python,
            generate_python_construct=args.generate_python_construct)

