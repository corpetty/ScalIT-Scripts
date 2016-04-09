__author__ = 'Corey Petty'
import itertools
import file_parse.get_parameters as get_params
from triatomic_mod import dict_to_class
from triatomic_mod import set_environment as env
from util import environment
import posixpath
import re
import csv
from triatomic_mod.molecule import Molecule
from triatomic_mod.options import Options


def format_mathematica(mol: Molecule, opts: Options, parameter_sets: list, eig_list: list) -> list:
    formatted_eig_list = []
    for num, eigs in enumerate(eig_list):
        formatted_eig_string = "%(mass_option)sJ%(jtot)dr%(lr)dR%(br)dgm%(gm)d%(perm)s%(parity)s = {" \
            % {'mass_option': mol.mass_combo,
               'jtot': parameter_sets[num][0],
               'lr': parameter_sets[num][1],
               'br': parameter_sets[num][2],
               'gm': min(opts.hin_options.num_res_angles, parameter_sets[num][3]),
               'perm': mol.permutation,
               'parity': mol.parity
               }
        for eig in eigs:
            formatted_eig_string += str(eig).replace("E|e|D", "*^") + ", "
        formatted_eig_string = re.sub(", $", "};\n", formatted_eig_string)
        formatted_eig_list.append(formatted_eig_string)
    return formatted_eig_list


def format_csv(mol: Molecule, opts: Options, parameter_sets: list, eig_list: list, err_list: list):
    from util.general_functions import check_csv_duplicates
    filename = mol.name + "states.csv"
    with open(filename, mode='a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['mass_label', 'J_total', 'j_max', 'num_lr', 'num_br', 'num_gm', 'permutation', 'parity',
                             'lanczos_error', 'num_states', 'states'])
        for num, eigs in enumerate(eig_list):
            formatted_eig_string = ""
            for eig in eigs:
                formatted_eig_string += str(eig).replace("E|e|D", "*^") + ", "
            formatted_eig_string = formatted_eig_string[:-2]
            filewriter.writerow([mol.mass_combo, parameter_sets[num][0], parameter_sets[num][4],
                                 parameter_sets[num][1], parameter_sets[num][2],
                                 min(parameter_sets[num][3], opts.hin_options.num_res_angles),
                                 mol.permutation, mol.parity, err_list[num], len(eigs),
                                 formatted_eig_string])
        print("Files written to {}\n".format(filename))
    print("Checking for duplicate entries and removing")
    check_csv_duplicates(filename)


def print_eigenvalues(params, variables) -> int:
    from ScriptIT import exit_func
    from file_parse.run_stats import get_lanczos_error
    #  instantiate choice for return.
    choice = None
    #  Get list of files to parse from run_parameters file
    files = environment.Files()
    outfiles = []
    parameter_sets = []
    (paths, mol, opts, mpienv) = dict_to_class.create_class(params=params)
    basis_sizes = list(itertools.product(*variables[1:]))
    for jtot in variables[0]:
            mol.j_total = jtot
            env.generate_paths(directories=paths, molecule=mol)
            for lr, br, jmax in basis_sizes:
                mol.lr.num_dvr_fns = lr
                mol.br.num_dvr_fns = br
                mol.j_max = jmax
                mol.get_num_angles()
                env.generate_filenames(files=files, molecule=mol)
                outfiles.append(paths.run + '/' + files.iterate + files.output)
                parameter_sets.append([jtot, lr, br, mol.jk_num, mol.j_max])

    #  check existence of outfiles, remove if not in existence
    for num, outfile in enumerate(outfiles):
        if not posixpath.exists(outfile):
            outfiles.remove(outfile)
            parameter_sets.remove(parameter_sets[num])
            print("{} is not formatted correctly, skipping it".format(outfile))

    #  extract eigenvalues from easy in above list
    eig_list = []
    err_list = []
    for outfile in outfiles:
        try:
            err_list.append(get_lanczos_error(outfile))
            eig_list.append(get_params.eigenvalues(outfile=outfile))
        except (FileNotFoundError, IOError):
            print("{} not found, wasn't run")
            pass

    while choice != -1:
        #  Get choice from user on desired output
        print("Please choose desired form of output: ")
        print("    (1)  Print mathematica friendly eigenvalues to screen")
        print("    (2)  Create/append to database file (.csv)")
        print("    (-1) Return to main menu")
        print("    (0)  Exit")
        choice = int(input("Please input choice: "))
        print("\n")

        if choice == 1:
            formatted_eig_list = format_mathematica(mol, opts, parameter_sets, eig_list)
            #  print to screen
            for num, eigs in enumerate(formatted_eig_list):
                print("Lanczos Error: " + err_list[num])
                print(eigs)
        elif choice == 2:
            format_csv(mol, opts, parameter_sets, eig_list, err_list)
        elif choice == 0:
            print("Exiting")
            exit_func()
        elif choice == -1:
            print("Returning to main menu")
        else:
            print("Please choose from one of the above options.")
    return choice
