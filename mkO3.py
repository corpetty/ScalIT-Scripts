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
#   version < 0: mpi program without parallel IO (currently best for HPCC environment)
#   version > 0: mpi program with parallel IO
#
#############################################################################################################
run_options = dict(
    version=0,
    conv_option=2,
    nvar=[30, 35, 40],       # values of convergence parameter, list length specifies how many jobs in script
    jmax=120,
    ngi=300,               # default value
    ndvr=[30, 30, 0],        # ndvr[2] will be set later
    nodes_desired=1,         # number of nodes requested for mpi job.  Number of cores depends on platform
    local_cores=4            # if dirs['host'] is 'local', number of cores desired to run mpi jobs
)


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
mol = dict(
    Name='ozone',
    permutation='o',
    mass=(14578.471659, 9718.981106),
    Rmin=(1.5, 0.0), Nmax=(6000, 6000),
    Rmax=(6.0, 5.0), Nmin=(40, 60),
    re=(2.401, 1.256),
    parity='T',
    useSP='T',
    jtotal=0,
    dvr_type=2
)
#############################################################################################################
#        Directories
#    NOTE: end all with a /
#############################################################################################################
dirs = dict(
    host='local',
    home='/Users/coreypetty/',
    data='/Users/coreypetty/work/data/',
    scalit='/Users/coreypetty/work/ScalIT-ozone/'
)
#############################################################################################################
#           Misc. parameters
#############################################################################################################
hin_flags = dict(
    FcFlag=0,       # Fixed Coordinates Flag,           0 : None
    CbFlag=0,       # Combined Basis Flag,              0 : None
    AbsFlag=0,      # Absorbtion Potentials Flag,       0 : None
    Ecutoff=0.1,    # Energy Cutoff Value (a.u. for Ozone)
    ReFlag=0        # Store/Extract equilibrium values, 0 : Neither
)
#############################################################################################################
#          parameters for *.in file
#############################################################################################################
in_options = dict(
    ndvr='',                                    # dimensionality for each layer, defined elsewhere
    opt0='F F F\n',                             # coordinator dependence
    opt1='1 0\n',                               # "task osb_preconditioner"
    opt2='F T F F\n',                           # "store_all complex "
    bjQMR='10 1.0D-3 10000 1.0D-3\n',           # block_Jacobi/QMR "bjNum bjToler qmrNum qmrToler"
    pistConv='0.0 1.0D-9 50 10 400 30 5\n',     # PIST convergence "E0 LancToler nStart nStep nMax nNum nGap"
    nState='0.0 1.0D-3 10.0 1000\n',            # OSB parameters "mE0 mDE mBeta nCnt
    fh0='',                                     # store H0 filename
    fhgm='',                                    # store Hgm filename
    fpt='',                                     # store wave function filename
    opt3='0 0 0 0 0\n',                         # do not save wave function
)
#############################################################################################################
# Actual routine call DO NOT CHANGE
Triatomic.MakeFiles.mka3(run_options, mol, hin_flags, dirs, in_options)