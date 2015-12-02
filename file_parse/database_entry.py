__author__ = 'Corey Petty'
import pandas as pd
from file_parse.get_parameters import combined_dict_from_inputs
from file_parse.get_parameters import eigenvalues


def print_table(hinfilename, infilename, outfilename) -> pd.DataFrame:
    # get isotope
    isotope = input("Please input the isotopologue of input files: ")

    # get run parameters from input files
    param_dict = combined_dict_from_inputs(hinfilename, infilename)

    # Get states from *.out
    eig_list = eigenvalues(outfilename)

    # Get permuatation symmetry
    permutation = ()

    # Create state index

    # Submit entry of states
    dummy = []

    # Format into table
    #  "isotope, Permutation, J_total, j_max, Num_lr, Num_br, Num_theta, Parity, State_index, Energy "
    for num, state in enumerate(eig_list, 1):
        dummy.append([isotope, param_dict["J_total"], param_dict["j_max"],
                      param_dict["num_lr"], param_dict["num_br"],
                      param_dict["num_gm"], param_dict["parity"],
                      param_dict["pist_e0"], num, state])

    df = pd.DataFrame(dummy, columns=["isotope", 'J Total', 'j max',
                                      'num lr', 'num br', 'num gm',
                                      'parity', 'central energy', 'state index', 'state'])

    return df
