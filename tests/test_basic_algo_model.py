import itemlang.algoc.metamodel as algo_metamodel
from textx import children_of_type

def test_basic_algo_model():
    mm=algo_metamodel.get_meta_model();
    model = mm.model_from_str("""
    package data {
        type int {}
        type float  {}
        struct Data {
            scalar n: int { default="10" }
            array a: float[n]
        }
    }
    algo_package test {
        algo Adder {
            in      a: data.Data // input
            inout   b: data.Data // b = a+b
            out     c: data.Data // == b
        }
    }
    """)

    algos = children_of_type("Algo", model)
    assert len(algos)==1

    algo = algos[0]
    inputs = children_of_type("AlgoIn", algo)
    assert len(inputs)==1
    assert inputs[0].name == "a"

    inouts = children_of_type("AlgoInOut", algo)
    assert len(inouts)==1
    assert inouts[0].name == "b"

    outputs = children_of_type("AlgoOut", algo)
    assert len(outputs)==1
    assert outputs[0].name == "c"

    assert outputs[0].type == inputs[0].type
    assert outputs[0].type == inouts[0].type
