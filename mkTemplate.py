__author__ = 'coreypetty'
# !/usr/bin/env python

import Triatomic.MakeFiles

#############################################################################################################
# do convergence testing for tri-atomic molecules.
# parameters: J, r, BR, jmax, nA0
#
# conv_option < 0: generate files for *.pin
#
# conv_option = [0-1], fix J, r, R
# conv_option = 0: jmax convergence testing
# conv_option = 1: Combined angular basis convergence testing
#
# conv_option = [2-3], fix jmax, nA0
# conv_option = 2: fix R;       r convergence testing
# conv_option = 3: fix r;       R convergence testing
#
# other options: fix jmax, r, R; variable of J Total
#
# VERSION: which program
#   VERSION = 0: sequential
#   VERSION < 0: mpi program without parallel IO (currently best for HPCC environment)
#   VERSION > 0: mpi program with parallel IO
#
#############################################################################################################

conv_option = 0
VERSION = 0

jmax = [60]
ngi = [100]
ndvr = [30, 30, 0]
nvar = [110, 120, 130]


#############################################################################################################
#   Molecular Parameters
#
#   Name:           name of molecular system as ScalIT sees it
#   permutation:    permutation symmmetry
#                       'e' : even
#                       'o' : odd
#   mass:           reduced masses for little r and Big r
#   re:             equilibrium distances for little r and Big R
#   Rmin:           minimum distance in coordinate range for little r and Big R
#   Rmax:           maximum distance in coordinate range for little r and Big R
#   Nmax:           maximum number of sinc functions used in PRESINC module, for little r and Big R
#   Nmin:           number of VBR functions solved for in PRESINC module for little r and Big R
#   parity:         chosen parity of system
#                       'T' : even
#                       'F' : odd
#   useSP:          flag to choose whether splines are used to create 1D eff potentials
#                       'T' : True, use splines stored in
#                             ScalIT/src/data/<Name>/
#                       'F' : False, use analytic functions provided in
#                             ScalIT/src/systems/<Name>/pot_<Name>.f90
#   jtotal:         Total angular momentum quantum number, J
#   dvrType:        Type of sinc DVR to use
#                       1 : normal sinc DVR, centered around 0
#                       2 : radial sinc DVR
#############################################################################################################
mol = {
    'Name': '',                 # Fill in as ScalIT calls it, i.e. ho2
    'permutation': '',          # 'e' or 'o'
    'mass': (0.0, 0.0),         # (lr, BR)
    'Rmin': (0.0, 0.0),         # (lr, BR)
    'Rmax': (0.0, 0.0),         # (lr, BR)
    'Nmax': (6000, 6000),       # default (lr, BR)
    'Nmin': (80, 80),           # default (lr, BR)
    'parity': '',               # 'T' or 'F'
    'useSP': '',                # 'T' or 'F'
    'jtotal': 0,                # default, vibrational
    'dvrType': 2                # deafult, radial sinc DVR
}
#############################################################################################################
#        Directories
#    NOTE: end all with a /
#############################################################################################################
dirs = {
    'host': 'PettyMBP',  # host options: PettyMBP, Hrothgar, Robinson, Lonestar
    'home': '/Users/coreypetty/',
    'data': '/Users/coreypetty/work/data/',
    'scalit': '/Users/coreypetty/work/ScalIT-ozone/',
    'psodata': '/Users/coreypetty/work/data/psovbr/'
}

dirs['bin'] = dirs['scalit'] + 'bin/'
dirs['pes'] = dirs['scalit'] + 'src/systems/'
dirs['work'] = dirs['scalit'] + 'work/test/'
dirs['pesData'] = dirs['scalit'] + 'data/'

#############################################################################################################
#          commands in MPI
#############################################################################################################
cmd = {
    'np': '$NSLOTS',
    'wtime': '5:0:0'
}

if VERSION == 0:  # Sequential program
    cmd['mpi'] = ''
elif dirs['host'] == 'Hrothgar':  # options in hrothgar cluster
    cmd['mpi'] = 'mpirun -np %(np)d -machinefile mach.$$' % {'np': cmd['np']}
# TODO: add Lonestar, Robinson, PettyMBP to MPI commands

bin_dir = dirs['bin'] + mol['Name'] + '/'
if VERSION == 0:  # sequential program
    cmd['hin'] = bin_dir + mol['Name'] + '_' + mol['permutation']
    cmd['in'] = dirs['bin'] + 'iterate'
elif VERSION < 0:  # MPI 1
    cmd['hin'] = bin_dir + 'p' + mol['Name'] + '_' + mol['permutation']
    cmd['in'] = dirs['bin'] + 'p_iterate'
else:  # MPI 2, Parallel IO
    cmd['hin'] = bin_dir + 'm' + mol['Name'] + '_' + mol['permutation']
    cmd['in'] = dirs['bin'] + 'm_iterate'

#############################################################################################################
#           Misc. parameters
#############################################################################################################
hin_flags = {
    'FcFlag': 0,                                # Fixed Coordinates Flag,           0 : None
    'CbFlag': 0,                                # Combined Basis Flag,              0 : None
    'AbsFlag': 0,                               # Absorbtion Potentials Flag,       0 : None
    'Ecutoff': 0.1,                             # Energy Cutoff Value (a.u. for Ozone)
    'ReFlag': 0                                 # Store/Extract equilibrium values, 0 : Neither
}

#############################################################################################################
#          parameters for *.in file
#############################################################################################################
in_options = {
    'ndvr': '',                                 # dimensionality for each layer
    'opt0': 'F F F\n',                          # coordinator dependence
    'opt1': '1 0\n',                            # "task osb_preconditioner"
    'opt2': 'F T F F\n',                        # "store_all complex "
    'bjQMR': '10 1.0D-3 10000 1.0D-3\n',        # block_Jacobi/QMR "bjNum bjToler qmrNum qmrToler"
    'pistConv': '0.0 1.0D-9 50 10 400 30 5\n',  # PIST convergence "E0 LancToler nStart nStep nMax nNum nGap"
    'nState': '0.0 1.0D-3 10.0 1000\n',         # OSB parameters "mE0 mDE mBeta nCnt
    'fh0': '',                                  # store H0 filename
    'fhgm': '',                                 # store Hgm filename
    'fpt': '',                                  # store wave function filename
    'opt3': '0 0 0 0 0\n',                      # do not save wave function
}

#############################################################################################################
# Actual routine call DO NOT CHANGE
Triatomic.MakeFiles.mka3(conv_option, cmd, mol, hin_flags, dirs, in_options, jmax, ngi, ndvr, nvar)