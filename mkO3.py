__author__ = 'Corey Petty'
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
# version: which program
# version = 0: sequential
# version < 0: mpi program without parallel IO (currently best for HPCC environment)
# version > 0: mpi program with parallel IO
#
#############################################################################################################
run_opts = dict(
    version=-1,
    conv_option=-1,
    nvar=[120, 130, 140],       # values of convergence parameter, list length specifies how many jobs in script
    nodes_desired=1,            # number of nodes requested for mpi job.  Number of cores depends on platform
    local_cores=4,              # if dirs['host'] is 'local', number of cores desired to run mpi jobs
    run_time='48:00:00'         # used if host == Lonestar (hrs:mins:sec)
)


#############################################################################################################
#   Molecular Parameters
#
#   Name:           name of molecular system as ScalIT sees it
#   mass:           reduced masses for little r and Big r
#   re:             equilibrium distances for little r and Big R
#   Rmin:           minimum distance in coordinate range for little r and Big R
#   Rmax:           maximum distance in coordinate range for little r and Big R
#############################################################################################################
mol = dict(
    Name='ozone',
    mass=(14578.471659, 9718.981106),
    Rmin=(1.5, 0.0),
    Rmax=(6.0, 5.0),
    re=(2.401, 1.256),
)
#############################################################################################################
#           Relevant User Directories
#    NOTE: DO NOT end directories with a "/", this will be added when necessary
#    host options: local, Robinson, Hrothgar, Lonestar
#############################################################################################################
dirs = dict(
    host='Lonestar',
    work='/work/01670/corpetty/work/ozone',
    home='/home1/01670/corpetty',
    data='/scratch/01670/corpetty/DataFiles',
    scalit='/work/01670/corpetty/ScalIT-ozone'
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
pin_opts = dict(
    dvr_type=2,
    useSP='T',
    num_sinc_fns=[6000, 6000],
    max_DVR_fns=[80, 80]
)
#############################################################################################################
#           Hamiltonian Construction (*.hin file) Parameters
#
#   jtotal:                     Total angular momentum quantum number, J
#   jmax:                       Number of basis functions associated with little j
#   permutation:                Permutation symmmetry
#                                   'e' : even
#                                   'o' : odd
#   parity:                     Chosen parity of system
#                                   'T' : even
#                                   'F' : odd
#   num_lr_functions:           Desired number of basis functions in lr coordinate
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
#   Ecutoff:                    Energy Cutoff Value (a.u. for Ozone)
#   ReFlag:                     Store/Extract equilibrium values,
#                                   0 : Neither
#############################################################################################################
hin_opts = dict(
    j_total=0,
    jmax=130,
    permutation='o',
    parity='T',
    num_lr_functions=30,
    num_Br_functions=30,
    restrict_num_angles='T',
    num_angles=50,
    ngi=300,
    FcFlag=0,
    CbFlag=0,
    AbsFlag=0,
    Ecutoff=0.1,
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
in_opts = dict(
    opt0='F F F\n',
    opt1='1 0\n',
    opt2='F T F F\n',
    bjQMR='10 1.0D-3 10000 1.0D-3\n',
    pistConv='0.0 1.0D-9 50 10 400 30 5\n',
    nState='0.0 1.0D-3 10.0 1000\n',
    opt3='0 0 0 0 0\n',
)
# TODO: Create descriptions for all these
in_opts2 = dict(
    sDep=['F', 'F', 'F'],
    sJOB=1,
    sOSB=0,
    sCX='F',
    sNDVR='T',
    sST='T',
    sAP='F',
    bj_NumberIters=10,
    bj_Tolerance='1.0D-3',
    qmr_NumberIters=10000,
    qmr_Tolerance='1.0D-3',
    pist_E0=0.0,
    pist_LancToler='1.0D-9',
    pist_nStart=50,
    pist_nStep=10,
    pist_nMax=400,
    pist_nGap=5,
    osb_mE0=0.0,
    osb_mDE='1.0D-3',
    osb_mBeta=1.0,
    osb_nCnt=1000,
    sHOSB=0,
    sVOSB=0,
    sHW=0,
    sVX=0,
    sPT=0
)
# TODO: Create descriptions for all these
in_file_names = dict(
    fH0='',
    fRES='',
    fDep=['', '', ''],
    fAPP='',
    fAPR='',
    fHOSB='',
    fVOSB='',
    fEig='',
    fHW='',
    fVX='',
    fPT=''
)
#############################################################################################################
# Actual routine call DO NOT CHANGE
params = dict(
    run_opts=run_opts,
    pin_opts=pin_opts,
    hin_opts=hin_opts,
    in_opts=in_opts,
    mol=mol,
    dirs=dirs
)
Triatomic.MakeFiles.mka3(params)
