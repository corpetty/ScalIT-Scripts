__author__ = 'Corey Petty'
import itertools
import run_parameters as rp
import file_parse.get_parameters as get_params
from triatomic_mod import dict_to_class
from triatomic_mod import set_environment as env
from util import environment


def print_eigenvalues():
    #  Get list of files to parse from run_parameters file
    files = environment.Files()
    outfiles = []
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
                outfiles.append(paths.run + '/' + files.iterate + files.output)

    #  check existence of outfiles, remove if not in existence

    #  extract eigenvalues from easy in above list
    eig_list = []
    for outfile in outfiles:
        eig_list.append(get_params.eigenvalues(outfile=outfile))
    for eigs in eig_list:
        print(eigs)

    #  format each list into mathematica ready input
    formatted_eig_string = "%(mass_option)sJ%(jtot)dr$(lr)dR%(br)d%(gm)d%(perm)s%(parity)s = {" \
        % {'mass_option': mol.mass_combo,
           'jtot': mol.j_total,
           'lr': mol.lr.num_dvr_fns,
           'br': mol.br.num_dvr_fns,
           'gm': min(opts.hin_options.num_res_angles, mol.jk_num),
           'perm': mol.permutation,
           'parity': mol.parity
           }
    formatted_eig_list = []
    for eigs in eig_list:
        for eig in eigs:
            formatted_eig_string += str(eig).replace("E|e|D", "*^") + ", "
        formatted_eig_string[-2:] = "};"
        formatted_eig_list.append(formatted_eig_string)

    #  print to screen
    for eigs in formatted_eig_list:
        print(eigs)
