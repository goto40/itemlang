# System tests

Here we make a system test including the code generator and other compilers.

## File structure

    ------------------------------------------------
    cpp : cmake based C++ subproject (tests, algos)
    ------------------------------------------------

        The cmake project generates code from the model
        Input:                  model files
        Intermediate output:    code in src-gen
        Output:                 a library (Algo.lib.a)
        Output:                 unittests (Tester.exe)

    cpp/catch   : (dependency)
    cpp/GSL     : (dependency)
    cpp/src     : library code (algos)
    cpp/tests   : unittest
    cpp/src-gen : (generated code)
    cpp/build   : (created by run.sh)


    ------------------------------------------------
    model : model data, used by other submodels
    ------------------------------------------------

    model/items : item models
    model/algos : algo models


## Get the project

    $ git clone https://github.com/goto40/itemlang --recurse-submodules 


## Build and run

    $ sh run.sh # (Linux)

