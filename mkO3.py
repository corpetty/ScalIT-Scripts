__author__ = 'coreypetty'
# !/usr/bin/env python
#
# do convergence testing for tri-atomic molecules.
# parameters: J, r1, r2, BR, j1, j2, j12, nA0
#
# conv_option<0: generate files for *.pin
#
# conv_option = [0~4], fix J, r1, r2, R
# conv_option = 0: fix j12,nA0; j1=j2; j12=j1+j2, convergence testing
# conv_option = 1: fix j2,j12,nA0;     j1 convergence testing
# conv_option = 2: fix j1,j12,nA0;     j2 convergence testing
# conv_option = 3: fix j1,j2, nA0;     j12 convergence testing
# conv_option = 4: fix j1,j2,j12;      nA0 convergence testing
#
# opt=[10-14], fix j1, j2, j12, nA0
# conv_option = 10: fix R,       r1=r2 convergence testing
# conv_option = 11: fix r2,R;    r1 convergence testing
# conv_option = 12: fix r1,R;    r2 convergence testing
# conv_option = 13: fix r1,r2,;  R convergence testing
#
# other options: fix j1, j2, j12, r1, r2, R, variable of J
#
# VERSION: which program
#      0: sequence code
#   -1/1: hrothgar cluster with GE
#   -2/2: hrothgar cluster with InfiniBand
# others: NOTHING CURRENT
#
# VERSION = 0: sequential
# VERSION < 0: mpi program without parallel IO
# VERSION > 0: mpi program with parallel IO
#

import Triatomic.MakeFiles

conv_option = 0
VERSION = 0

jmax = [60]
ngi = [100]
ndvr = [30, 30, 0]
nvar = [110, 120, 130]


##################################################
#      mass, equilibrium, dvr points             #
#         A(3): data for lr1, lr2, BR            #
#      r range, Original Nmax, final NDVR        #
##################################################
mol = {
    'Name': 'ozone',
    'permutation': 'o',  # permutation symmetry
    'mass': (14578.471659, 9718.981106),  # mlr,mBR
    're': (2.401, 1.256),  # relr,reBR
    'Rmin': (1.5, 0.0), 'Nmax': (6000, 6000),
    'Rmax': (6.0, 5.0), 'Nmin': (40, 60),

    'parity': 'T', 'useSP': 'T',
    'jtotal': 0, 'dvrType': 2
}
##############################
#        Directories         #
#    NOTE: end all with a /  #
##############################
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

###################################
#          commands in MPI        #
###################################
cmd = {
    'np': '$NSLOTS',
    'wtime': '5:0:0'
}

if VERSION == 0:  # Sequential program
    cmd['mpi'] = ''
elif dirs['host'] == 'Hrothgar':  # options in hrothgar cluster
    cmd['mpi'] = 'mpirun -np %(np)d -machinefile mach.$$' % {'np': cmd['np']}
# add Lonestar, Robinson, PettyMBP

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

##########################################
#           Misc. parameters             #
##########################################
hin_flags = {'FcFlag': 0, 'CbFlag': 0, 'AbsFlag': 0, 'Ecutoff': 0.1, 'ReFlag': 0}

###############################################
#          parameters for *.in file           #
###############################################
in_options = {
    'ndvr': '',                                 # dimensionality for each layer
    'opt0': 'F F F\n',                          # coordinator dependence
    'opt1': '1 0\n',                            # "task osb_preconditioner"
    'opt2': 'F T F F\n',                        # "store_all complex "
    'bjQMR': '1000 1.0D-5 10000 1.0D-3\n',      # block_Jacobi/QMR "bjNum bjTol qmrNum qmrTol"
    'pistConv': '0.0 1.0D-4 50 10 200 30 5\n',  # PIST convergence
    'nState': '0.0 1.0D-3 10.0 1000\n',         # "nStart nStep nMax nNum nGap"
    'fh0': '',                                  # store H0
    'fhgm': '',                                 # store Hgm
    'fpt': '',                                  # store wave function
    'opt3': '0 0 0 0 0\n',                      # do not save wave function
}

# Actual routine call DO NOT CHANGE
Triatomic.MakeFiles.mka3(conv_option, cmd, mol, hin_flags, dirs, in_options, jmax, ngi, ndvr, nvar)