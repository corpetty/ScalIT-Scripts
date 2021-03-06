import sys
import triatomic_mod.convergence_tests
import tetraatomic_mod.convergence_tests
from triatomic_mod.parameter_file_utils import print_run_variables
from file_parse import structure_outfiles
from triatomic_mod.notify import check_rp_errors
import importlib
__author__ = 'Corey Petty'


def main(filename: str):
    if filename[-3:] == '.py':
        rp = importlib.import_module(filename[:-3])
    else:
        rp = importlib.import_module(filename)
    print_run_variables(params=rp.params, variables=rp.variables)

    #  Check to see if run parameters have errors
    if check_rp_errors(params=rp.params, variables=rp.variables):
        exit_func()

    choice = None
    while choice != 0:
        print_main_menu()
        choice = int(input("\nYour choice: "))
        print('\n')

        if choice == 1:
            if rp.params['molecule_size'] == 4:
                tetraatomic_mod.convergence_tests.multiple_run_from_dict(params=rp.params, variables=rp.variables)
            else:
                triatomic_mod.convergence_tests.multiple_run_from_dict(params=rp.params, variables=rp.variables)
            choice = 0
        elif choice == 2:
            choice = structure_outfiles.print_eigenvalues(params=rp.params, variables=rp.variables)
        elif choice == 0:
            exit_func()
        elif choice == -1:
            print_main_menu()
        else:
            print(" Please choose from the above options")
    exit_func()


def print_main_menu():
    print("=== ScriptIT Main Menu ===\n")
    print("Please choose from one of the following options:")
    print("    (1) Create input/run scripts")
    print("    (2) Collect eigenvalues from completed ScalIT jobs")
    print("    (0) Exit")


def exit_func():
    print("\n===========================================================================")
    print("\nExiting program")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1])
