__author__ = 'Corey Petty'
import util.general_functions as general_functions
from os import path


def eigenvalues(outfile: str) -> list:
    eig_list = []
    with open(outfile, mode='r') as f:
        for num, line in enumerate(f, 1):
            if "Max Lanczos" in line:
                break
        for line in f:
            if "---" in line:
                break
            for eig in line.split():
                eig_list.append(float(eig))
    # print("The eigenvalues are:")
    # for eig in eig_list:
    #     print('\t{:E}'.format(eig))
    return eig_list


def combined_dict_from_inputs(hinfilename: str, infilename: str) -> dict:
    template_path = path.dirname(general_functions.__file__)
    hin_dict = general_functions.dict_from_file_template(hinfilename, template_path + "/../File Templates/hin.template")
    in_dict = general_functions.dict_from_file_template(infilename, template_path + "/../File Templates/in.template")
    return_dict = {}
    return_dict.update(hin_dict)
    return_dict.update(in_dict)
    return return_dict


def permutation(scriptfilename: str) -> str:
    with open(scriptfilename, mode='r') as scriptfile:
        for line in scriptfile:
            for word in line.split():
                print(word)
                if "$BIN_DIR/" in word:
                    print(word[-1])
