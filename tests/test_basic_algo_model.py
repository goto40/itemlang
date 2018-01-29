import itemlang.algoc.metamodel as algo_metamodel
from textx import children_of_type
from pytest import raises
from os.path import join, dirname, abspath

def test_basic_algo_model():
    this_folder = dirname(abspath(__file__))
    mm=algo_metamodel.get_meta_model();
    model = mm.model_from_file(join(this_folder, "algos/simple_model.algo"))

    algos = children_of_type("Algo", model)
    assert len(algos)==1
    algo = algos[0]

    assert len(algo.get_all_structs_of_arguments())==1
    assert algo.get_all_structs_of_arguments()[0].name == "Data"
