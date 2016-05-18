__author__ = 'Corey Petty'
import util.general_functions as general_functions
from os import path


def combined_dict_from_inputs(hinfilename: str, infilename: str) -> dict:
    template_path = path.dirname(general_functions.__file__)
    hin_dict = general_functions.dict_from_file_template(hinfilename, template_path + "/../File Templates/hin.template")
    in_dict = general_functions.dict_from_file_template(infilename, template_path + "/../File Templates/in.template")
    return_dict = {}
    return_dict.update(hin_dict)
    return_dict.update(in_dict)
    return return_dict


