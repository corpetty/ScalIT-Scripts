__author__ = 'Corey Petty'

import posixpath
import os


class Directories(object):
    """
    Class object that simply holds all relavent ScalIT directory locations
    """
    def __init__(self, work="work", data="data", scalit="ScalIT"):
        self.work = work
        self.data = data
        self.scalit = scalit


class Files(object):
    pass


def generate_paths(paths, mol):
    """

    :param paths: Directories class
    :param mol:   Molecules class
    :return:
    """

    #  ScalIT Paths
    paths.bin = paths.scalit + "/bin"
    paths.pes_data = paths.scalit + "/data/" + mol.name

    #  Runtime Paths
    paths.run = paths.work + '/' + mol.name + '/' + mol.mass_combo + '/J' \
        + str(mol.j_total) + '/' + mol.permutation
    paths.run_psovbr = paths.work + '/' + mol.name + '/' + mol.mass_combo \
        + '/psodvr'

    #  Data Paths
    paths.run_data = paths.data + '/' + mol.name + '/' + mol.mass_combo + '/J' \
        + str(mol.j_total) + '/' + mol.permutation
    paths.run_psovbr_data = paths.data + '/' + mol.name + '/' + mol.mass_combo \
        + '/psodvr'

    check_existence(paths=paths)


def generate_filenames(files, mol):
    #  Affixes
    files.input = "in"
    files.output = "out"

    #  Step One Input/Output File Extention Prefix
    files.presinc_lr = "lr.p"
    files.presinc_br = "BR.p"

    #  Step One Output Data Files
    files.psovbr_lr = "vbr_lr.dat"
    files.psovbr_br = "vbr_BR.dat"

    #  Effective Potential Spline-Data File Names
    files.v_eff_lr = mol.name + "_vlr.dat"
    files.v_eff_br = mol.name + "_vBR.dat"

    #  Step Two Input/Output File Extention Prefix
    files.hamiltonian = "r%(lr)dR%(br)dgm%(gm)d%(par)s.h"\
                        % {'lr': mol.lr.num_dvr_fns,
                           'br': mol.br.num_dvr_fns,
                           'gm': mol.j_max,
                           'par': mol.permutation
                           }

    #  Step Two Output Data Files
    files.radial_ham = "H0-r%(lr)dR%(br)dgm%(gm)d%(par)s.dat"\
                       % {'lr': mol.lr.num_dvr_fns,
                          'br': mol.br.num_dvr_fns,
                          'gm': mol.j_max,
                          'par': mol.permutation
                          }
    files.angular_ham = "H0gm-r%(lr)dR%(br)dgm%(gm)d%(par)s.dat"\
                        % {'lr': mol.lr.num_dvr_fns,
                           'br': mol.br.num_dvr_fns,
                           'gm': mol.j_max,
                           'par': mol.permutation
                           }

    #  Step Three Input/Output File Extension Prefix
    files.iterate = "r%(lr)dR%(br)dgm%(gm)d%(par)s."\
                    % {'lr': mol.lr.num_dvr_fns,
                       'br': mol.br.num_dvr_fns,
                       'gm': mol.j_max,
                       'par': mol.permutation
                       }

    #  Scripts for running files
    files.run_script = "r%(lr)dR%(br)dgm%(gm)d%(par)s.sh"\
                       % {'lr': mol.lr.num_dvr_fns,
                          'br': mol.br.num_dvr_fns,
                          'gm': mol.j_max,
                          'par': mol.permutation
                          }

    #  Script to run Step 1, PSOVBR data creation
    files.run_psovbr_script = "psovbr.sh"


def check_existence(paths):
    for key, value in vars(paths).items():
        if not posixpath.exists(value):
            print '    Creating: ' + value
            os.makedirs(value)
