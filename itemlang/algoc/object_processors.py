from textx import children_of_type

def check_model(model):
    algo_packages = children_of_type("AlgoPackage", model)
    item_packages = children_of_type("Package", model)
    if len(item_packages)>0 and len(algo_packages)>0:
        raise Exception("define either algorithms OR items in one model file ({})".format(model._tx_filename))