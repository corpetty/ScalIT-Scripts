from util import general_functions
__author__ = 'Corey Petty'

#  TODO: finish and implement (somehow)
def triatomic_load(molecule: object):
    chosen_system = input("Please type system to load: ")
    default_file = "Molecule Defaults/" + chosen_system + ".default"
    defaults_dict = general_functions.read_dict_from_file(default_file)
    for key, value in defaults_dict.items():
        setattr(molecule, key, value)
