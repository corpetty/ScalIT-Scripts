import sys
from triatomic_mod.convergence_tests import multiple_run_from_dict
from file_parse import outfiles_to_mathematica
import run_parameters as rp
__author__ = 'Corey Petty'


def main(argv):
    print("=== ScriptIT Main Menu ===\n")
    print("Please choose from one of the following options:")
    print("    (1) Create input/run scripts")
    print("    (2) Collect eigenvalues from completed ScalIT jobs")
    print("    (0) Exit")
    choice = None
    while choice != 0:
        choice = int(input("\nYour choice: "))

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


