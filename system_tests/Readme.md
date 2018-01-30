# System tests

Here we make a system test including the code generator and other compilers.

## Structure

    ------------------------------------------------
    cpp : cmake based C++ subproject (tests, algos)
    ------------------------------------------------

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


## Build & Run

    $ sh run.sh # (Linux)

