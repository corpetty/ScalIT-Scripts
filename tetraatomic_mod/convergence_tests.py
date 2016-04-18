import util.environment

__author__ = 'Corey Petty'

import tetraatomic_mod.dict_to_class as dict_to_class
import tetraatomic_mod.set_environment as env
import tetraatomic_mod.make_files as make_files
import tetraatomic_mod.make_scripts as make_scripts
import itertools
import os.path
# TODO: port over tetraatomic_mod.notify import check_if_using_ceiling


def multiple_run_from_dict(params, variables):
    print('*** CREATING FILES FOR MULTIPLE SCALIT RUNS ***')

    #  Instantiate and populate classes from dictionary
    (paths, mol, opts, platform) = dict_to_class.create_class(params=params)

    #  Instantiate Files class
    files = util.environment.Files()

    #  Create files for all combinations of basis functions
    basis_sizes = list(itertools.product(*variables[1:]))
    env.generate_paths(directories=paths, molecule=mol)
    env.generate_filenames(files=files, molecule=mol)
    if not os.path.exists(paths.run_psovbr_data + '/' + files.psovbr_lr1):
        print('   WARNING: PSOVBR metadata does not exist!  Be sure to run Step 1 first.')
        make_files.step_one(paths=paths, files=files, molecule=mol, pin_options=opts.pin_options)
        make_scripts.pin_script(directories=paths, files=files, molecule=mol)
    else:
        #  Display information to screen
        print('')
        print('----> Molecular information read from parameter file:')
        print('    Molecule:                  %(name)s' % {'name': mol.name})
        print('    Total J values:            %(jtot)s' % {'jtot': ', '.join(map(str, variables[0]))})
        print('    Little r values:           %(lr)s' % {'lr': ', '.join(map(str, variables[1]))})
        print('    Big R values:              %(br)s' % {'br': ', '.join(map(str, variables[2]))})
        print('    j_max values:              %(gm)s' % {'gm': ', '.join(map(str, variables[3]))})
        print('    Maximum angular functions: %(max)d' % {'max': opts.hin_options.num_res_angles})
        print('    Number of states desired:  %(num)d' % {'num': opts.in_options.pist_num_e0})
        print('    Central energy:            %(e0)G' % {'e0': opts.in_options.pist_e0})
        print('    Total run accuracy:        %(acc)G' % {'acc': opts.in_options.pist_lanc_tolerance})
        print('')
        print('    NOTE: All combinations of J, lr, br, and jmax values will be created\n')

        for jtot in variables[0]:
            mol.j_total = jtot
            env.generate_paths(directories=paths, molecule=mol)
            print('\n----> Generating files for J = %(J)d' % {'J': mol.j_total})
            for lr1, lr2, br, j1max, j2max in basis_sizes:
                mol.lr1.num_dvr_fns = lr1
                mol.lr2.num_dvr_fns = lr2
                mol.br.num_dvr_fns = br
                mol.j1_max = j1max
                mol.j2_max = j2max
                mol.get_num_angles()
                # check_if_using_ceiling(jk_num=mol.jk_num, angle_ceiling=opts.hin_options.num_res_angles)
                env.generate_filenames(files=files, molecule=mol)
                make_files.step_two(paths=paths, files=files, molecule=mol, options=opts)
                make_files.step_three(paths=paths, files=files, mol=mol, options=opts)
                make_scripts.run_script(directories=paths, files=files, molecule=mol, platform=platform, options=opts)
