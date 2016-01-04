__author__ = 'Corey Petty'
import itertools
import run_parameters as rp
import file_parse.get_parameters as get_params
from triatomic_mod import dict_to_class
from triatomic_mod import set_environment as env
from util import environment
import posixpath
import re


def print_eigenvalues():
    #  Get list of files to parse from run_parameters file
    files = environment.Files()
    outfiles = []
    parameter_sets = []
    (paths, mol, opts, mpienv) = dict_to_class.create_class(params=rp.params)
    basis_sizes = list(itertools.product(*rp.variables[1:]))
    for jtot in rp.variables[0]:
            mol.j_total = jtot
            env.generate_paths(directories=paths, molecule=mol)
            for lr, br, jmax in basis_sizes:
                mol.lr.num_dvr_fns = lr
                mol.br.num_dvr_fns = br
                mol.j_max = jmax
                mol.get_num_angles()
                env.generate_filenames(files=files, molecule=mol)
                outfiles.append(paths.run + '/' + files.iterate + "$JOB_ID." + files.output)
                parameter_sets.append([jtot, lr, br, mol.jk_num])

    #  check existence of outfiles, remove if not in existence
    for num, outfile in enumerate(outfiles):
        if not posixpath.exists(outfile):
            outfiles.remove(outfile)
            parameter_sets.remove(parameter_sets[num])

    #  extract eigenvalues from easy in above list
    eig_list = []
    for outfile in outfiles:
        eig_list.append(get_params.eigenvalues(outfile=outfile))

    #  format each list into mathematica ready input
    formatted_eig_list = format_mathematica(mol, opts, parameter_sets, eig_list)

    #  print to screen
    for eigs in formatted_eig_list:
        print(eigs)


def format_mathematica(mol, opts, parameter_sets: list, eig_list: list) -> list:
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
