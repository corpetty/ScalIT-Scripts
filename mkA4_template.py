__author__ = 'Corey Petty'
# !/usr/bin/env python

import Tetraatomic.MakeFiles

#############################################################################################################
# do convergence testing for tri-atomic molecules.
# parameters: J, r1, r2, BR, j1_max, j2_max, theta
#
# conv_option < 0: generate files for *.pin
#
# conv_option = [0-2], fix J, r, R
# conv_option = 0: j1 convergence testing
# conv_option = 1: j2 convergence testing
# conv_option = 2: Combined angular basis convergence testing (jkNum)
#
# conv_option = [3-5], fix jmax, nA0
# conv_option = 3: fix r2, R;       r1 convergence testing
# conv_option = 4: fix r1, R;       r2 convergence testing
# conv_option = 5: fix r1, r2;      R convergence testing
#
# other options: fix jmax, r, R; variable of J Total
#
# version: which program
# version = 0: sequential
# version < 0: mpi program without parallel IO (currently best for HPCC environment)
# version > 0: mpi program with parallel IO
#
#############################################################################################################
run_opts = dict(
    version=-1,
    conv_option=0,
    nvar=[0, 0, 0],             # values of convergence parameter, list length specifies how many jobs in script
    nodes_desired=1,            # number of nodes requested for mpi job.  Number of cores depends on platform
    local_cores=4,              # if dirs['host'] is 'local', number of cores desired to run mpi jobs
    run_time='48:00:00'         # used if host == Lonestar (hrs:mins:sec)
)


#############################################################################################################
#   Molecular Parameters
#
#   Name:           name of molecular system as ScalIT sees it
#   mass:           reduced masses for r1, r2, and R
#   re:             equilibrium distances for r1, r2, R
#   Rmin:           minimum distance in coordinate range for r1, r2, R
#   Rmax:           maximum distance in coordinate range for r1, r2, R
#############################################################################################################
mol = dict(
    Name='',
    mass=(0.0, 0.0, 0.0),
    Rmin=(0.0, 0.0, 0.0),
    Rmax=(0.0, 0.0, 0.0),
    re=(0.0, 0.0, 0.0),
)
#############################################################################################################
#           Relevant User Directories
#    NOTE: DO NOT end directories with a "/", it will be added when necessary
#    host options: local, Robinson, Hrothgar, Lonestar
#############################################################################################################
dirs = dict(
    host='local',
    home='~',                    # directory location of your home folder
    data='~/data',               # directory location of your data folder (where to store large files)
    scalit='~/ScalIT-ozone'      # directory location of your ScalIT installation
)
#############################################################################################################
#           PRESINC Construction (*.pin file) Parameters
#
#   dvrType:        Type of sinc DVR to use
#                       1 : normal sinc DVR, centered around 0
#                       2 : radial sinc DVR
#   useSP:          flag to choose whether splines are used to create 1D eff potentials
#                       'T' : True, use splines stored in
#                             ScalIT/src/data/<Name>/
#                       'F' : False, use analytic functions provided in
#                             ScalIT/src/systems/<Name>/pot_<Name>.f90
#   num_sinc_fns:   Number of original functions used to create PSOVBR functions
#   max_DVR_fns:    Number of VBR functions output from module.
#
#############################################################################################################
pin_opts = dict(                    # All set to default values
    dvr_type=2,
    useSP='T',
    num_sinc_fns=[6000, 6000, 6000],
    max_DVR_fns=[80, 80, 80]
)
#############################################################################################################
#           Hamiltonian Construction (*.hin file) Parameters
#
#   jtotal:                     Total angular momentum quantum number, J
#   jmax:                       Number of basis functions associated with little j
#   permutation:                Permutation symmmetry
#                                   'Agg' : j1, j2 even
#                                   'Auu' : j1, j2 odd
#                                   'Agu' : j1 even, j2 odd
#                                   'Aug' : j1 odd, j2 even
#   parity:                     Chosen parity of system
#                                   'T' : even
#                                   'F' : odd
#   num_r1_functions:           Desired number of basis functions in r1 coordinate
#   num_r2_functions:           Desired number of basis functions in r2 coordinate
#   num_Br_functions:           Desired number of basis functions in Br coordinate
#   restrict_num_angles:        Whether or not to truncate jkNum.
#                                   'F' : theta = jkNum
#                                   'T' : theta = num_angles
#   num_angles:                 Number of angles if the above flag = 'T'
#   ngi:                        Number of Gauss Integrals to use
#   FcFlag:                     Fixed Coordinates Flag,
#                                   0 : None
#   CbFlag:                     Combined Basis Flag,
#                                   0 : None
#   AbsFlag:                    Absorbtion Potentials Flag,
#                                   0 : None
#   Ecutoff:                    Energy Cutoff Value
#   ReFlag:                     Store/Extract equilibrium values,
#                                   0 : Neither
#############################################################################################################
hin_opts = dict(
    jtotal=0,
    j1_max=0,
    j2_max=0,
    j_max=0,
    permutation='Agg',
    parity='T',
    num_r1_functions=0,
    num_r2_functions=0,
    num_Br_functions=0,
    restrict_num_angles='T',
    num_angles=50,
    ngi=300,
    FcFlag=0,
    CbFlag=0,
    AbsFlag=0,
    Ecutoff=0.2,                # default to 0.2 a.u.
    ReFlag=0
)
#############################################################################################################
#          Diagonalization Step (*.in file) Parameters
# TODO: Fill in descriptions of all variables here
#   opt0:                coordinator dependence
#   opt1:                "task osb_preconditioner"
#   opt2:                "store_all complex "
#   bjQMR:               block_Jacobi/QMR
#                           "bjNum bjToler qmrNum qmrToler"
#   pistConv:            PIST convergence
#                           "E0 LancToler nStart nStep nMax nNum nGap"
#   nState:              OSB parameters
#                           "mE0 mDE mBeta nCnt"
#   opt3:                do not save wave function
#############################################################################################################
in_opts = dict(                                 # All set to default values
    opt0='F F F F\n',
    opt1='1 0\n',
    opt2='F T T F\n',
    bjQMR='10 1.0D-3 10000 1.0D-3\n',
    pistConv='0.0 1.0D-9 50 10 400 30 5\n',
    nState='0.0 1.0D-3 10.0 1000\n',
    opt3='0 0 0 0 0\n',
)
#############################################################################################################
# Actual routine call DO NOT CHANGE BELOW HERE
params = dict(
    run_opts=run_opts,
    pin_opts=pin_opts,
    hin_opts=hin_opts,
    in_opts=in_opts,
    mol=mol,
    dirs=dirs
)
Tetraatomic.MakeFiles.mka4(params)
