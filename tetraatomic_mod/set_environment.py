__author__ = 'Corey Petty'

import os
import posixpath


def generate_paths(directories, molecule):
    """

    :param directories: Directories class
    :param molecule:   Molecules class
    :return:
    """

    #  ScalIT Paths
    directories.bin = directories.scalit + "/bin"
    directories.pes_data = directories.scalit + "/data/" + molecule.name

    #  Runtime Paths
    directories.run = directories.work + '/' + molecule.name + '/' + molecule.mass_combo + '/J' \
        + str(molecule.j_total) + '/' + molecule.permutation
    directories.run_psovbr = directories.work + '/' + molecule.name + '/' + molecule.mass_combo \
        + '/psodvr'

    #  Data Paths
    directories.run_data = directories.data + '/' + molecule.name + '/' + molecule.mass_combo + '/J' \
        + str(molecule.j_total) + '/' + molecule.permutation
    directories.run_psovbr_data = directories.data + '/' + molecule.name + '/' + molecule.mass_combo \
        + '/psodvr'

    check_existence(paths=directories)


def generate_filenames(files, molecule):
    #  Affixes
    files.input = "in"
    files.output = "out"

    #  Step One Input/Output File Extention Prefix
    files.presinc_lr1 = "lr1.p"
    files.presinc_lr2 = "lr2.p"
    files.presinc_br = "BR.p"

    #  Step One Output Data Files
    files.psovbr_lr1 = "vbr_lr1.dat"
    files.psovbr_lr2 = "vbr_lr2.dat"
    files.psovbr_br = "vbr_BR.dat"

    #  Effective Potential Spline-Data File Names
    files.v_eff_lr1 = molecule.name + "_vlr1.dat"
    files.v_eff_lr2 = molecule.name + "_vlr2.dat"
    files.v_eff_br = molecule.name + "_vBR.dat"

    #  Step Two Input/Output File Extention Prefix
    files.hamiltonian = "r%(lr)dR%(br)djmax%(j1max)d%(par)s.h" \
                        % {'lr': molecule.lr1.num_dvr_fns,
                           'br': molecule.br.num_dvr_fns,
                           'j1max': molecule.j1_max,
                           'par': molecule.parity
                           }

    #  Step Two Output Data Files
    files.radial_ham = "H0-r%(lr)dR%(br)djmax%(jmax)d%(par)s.dat" \
                       % {'lr': molecule.lr1.num_dvr_fns,
                          'br': molecule.br.num_dvr_fns,
                          'jmax': molecule.j1_max,
                          'par': molecule.parity
                          }
    files.angular_ham = "H0gm-r%(lr)dR%(br)djmax%(jmax)d%(par)s.dat" \
                        % {'lr': molecule.lr1.num_dvr_fns,
                           'br': molecule.br.num_dvr_fns,
                           'jmax': molecule.j1_max,
                           'par': molecule.parity
                           }

    #  Step Three Input/Output File Extension Prefix
    files.iterate = "r%(lr)dR%(br)djmax%(jmax)d%(par)s." \
                    % {'lr': molecule.lr1.num_dvr_fns,
                       'br': molecule.br.num_dvr_fns,
                       'jmax': molecule.j1_max,
                       'par': molecule.parity
                       }

    #  Scripts for running files
    files.run_script = "r%(lr)dR%(br)djmax%(jmax)d%(par)s.sh" \
                       % {'lr': molecule.lr1.num_dvr_fns,
                          'br': molecule.br.num_dvr_fns,
                          'jmax': molecule.j1_max,
                          'par': molecule.parity
                          }

    #  Script to run Step 1, PSOVBR data creation
    files.run_psovbr_script = "psovbr.sh"


def check_existence(paths):
    for _, value in vars(paths).items():
        if not posixpath.exists(value):
            print('    Creating: ' + value)
            os.makedirs(value)
