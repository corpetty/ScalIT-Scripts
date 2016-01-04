import sys
from triatomic_mod.convergence_tests import multiple_run_from_dict
from file_parse import outfiles_to_mathematica
import importlib
__author__ = 'Corey Petty'


def main(argv: str):
    if argv[0][-3:] == '.py':
        rp = importlib.import_module(argv[0][:-3])
    else:
        rp = importlib.import_module(argv[0])
    print("=== ScriptIT Main Menu ===\n")
    print("Please choose from one of the following options:")
    print("    (1) Create input/run scripts")
    print("    (2) Collect eigenvalues from completed ScalIT jobs")
    print("    (0) Exit")
    choice = None
    while choice != 0:
        choice = int(input("\nYour choice: "))
        print('\n')

        if choice == 1:
            multiple_run_from_dict(params=rp.params, variables=rp.variables)
            choice = 0
        elif choice == 2:
            outfiles_to_mathematica.print_eigenvalues()
            choice = 0
        elif choice == 0:
            exit_func()
        else:
            print(" Incorrect choice, please choose from the above options")
    exit_func()


def exit_func():
    print("\n===========================================================================")
    print("\nExiting program")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
