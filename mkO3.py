# coding=utf-8
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
    conv_option=0,
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
    host='local',
    work='/Users/coreypetty/work/ozone',
    home='/Users/coreypetty',
    data='/Users/coreypetty/work/ozone/data',
    scalit='/Users/coreypetty/work/ScalIT-ozone'
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
#   j_total:                    Total angular momentum quantum number, J
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
#          Diagonalization Step (*.in file) Switches
#   sF:             Number of layers in Hamiltonian
#                       3 : If no radial dimensional combination is used (default)
#                       2 : If radial dimensional combination is used
#   sDep:           Whether or not coordinate dependancy exist
#                       'T' : exists
#                       'F' : does not exist (default)
#   sJOB:           Type of job to run
#                       1     : Bound states (default)
#                       2,3   : Resonance States (disabled currently)
#                       4,5,6 : CRP calculations (disabled currently)
#   sOSB:           Choice of OSB preconditioning
#                       1 : Simple OSB Preconditioning  (Eig − E0)^−1
#                       2 : First OSBD Preconditioning  (Eig − E0)^−1 or mDE^−1
#                       3 : Second OSBD Preconditioning (Eig − E0)^−1 or [(1−β)⋆DE+β(E−E0)]^−1
#                       4 : OSBW Preconditioning        (Eig − E0)^−1 or Hp^−1
#   sCX:            Whether matrices are complex
#                       'T' : matrices are complex
#                       'F' : matrices are not complex
#   sNDVR:          Whether DVR is used in outermost layer
#                       'T' : DVR is used in outermost layer
#                       'F' : DVR is NOT used in outermost layer
#   sST:            Whether off-diagonal matrices of HOSB are stored in memory
#                       'T' : matrices are stored in memory
#                       'F' : matrices are NOT stored
#   sAP:            Whether absorbtion potentials exist
#                       'T' : they exist
#                       'F' : they do NOT exist
#   sHOSB:          Whether to store or load HOSB data file
#                       < 0 : load HOSB data file
#                         0 : Do nothing
#                       > 0 : save HOSB data file
#   sVOSB:          Whether to store or load VOSB data file
#                       < 0 : load VOSB data file
#                         0 : Do nothing
#                       > 0 : save VOSB data file
#   sHW:            Whether to store or laod HW0 and OSBW data file
#                       < 0 : load data file
#                         0 : Do nothing
#                       > 0 : save data file
#   sVX:            Whether to store or load PIST initial vector data file
#                       < 0 : load data file
#                         0 : Do nothing
#                       > 0 : save data file
#   sPT:            Whether to store or load PIST final vector data file
#                       < 0 : load data file
#                         0 : Do nothing
#                       > 0 : save data file
#
#############################################################################################################
in_switches = dict(
    sF='3',
    sDep=['F', 'F', 'F'],
    sJOB='1',
    sOSB='0',
    sCX='F',
    sNDVR='T',
    sST='T',
    sAP='F',
    sHOSB='0',
    sVOSB='0',
    sHW='0',
    sVX='0',
    sPT='0'
)
#############################################################################################################
#          Diagonalization Step (*.in file) Switches
#
#   bj_NumberIters:     Number of iterations for Block-Jacobi diagonalization
#   bj_Tolerance:       Tolerance threshhold for Block-Jacobi diagonalization
#   qmr_NumberIters:    Number of iterations for QMR
#   qmr_Tolerance:      Desired tolerance for QMR
#   pist_E0:            Central energy for PIST (THIS IS WHERE YOUR EIGENVALUES WILL BE CENTERED ON)
#   pist_LancToler:     Error Tolerance for Lanczos (THIS IS OVERALL ERROR OF RUN)
#   pist_nStart:        Iteration that starts to check Lanczos tolerance
#   pist_nStep:         How many Lanczos iterations before rechecking for tolerance
#   pist_nMax:          Maximum number of Lanczos iterations before quitting
#   pist_nE0            The number of eigenvalues to be calculated
#   pist_nGap:          How many previous iterations to compare to for tolerance check
#   osb_mE0:            Central energy of Wyatt window (This Must be close to pist_E0)
#   osb_mDE:            Threshold energy to ...... TODO: explain this
#   osb_mBeta:          Parameter for OSBD, as can be seen in sOSB options
#   osb_nCnt:           Size of Wyatt energy window centered on osb_mE0
#
#############################################################################################################
in_parameters = dict(
    bj_NumberIters='10',
    bj_Tolerance='1.0D-3',
    qmr_NumberIters='10000',
    qmr_Tolerance='1.0D-3',
    pist_E0='0.0',
    pist_LancToler='1.0D-9',
    pist_nStart='50',
    pist_nStep='10',
    pist_nMax='400',
    pist_nE0='30',
    pist_nGap='5',
    osb_mE0='0.0',
    osb_mDE='1.0D-3',
    osb_mBeta='1.0',
    osb_nCnt='1000',
)
#############################################################################################################
#          Diagonalization Step (*.in file) Switches
#
#   fRES:
#   fDep:
#   fAPP:
#   fAPR:
#   fHOSB:
#   fVOSB:
#   fEig:
#   fHW:
#   fVX:
#   fPT:
#
#############################################################################################################
in_file_names = dict(
    fRES='fRES.dat',
    fDep=['fDep1.dat', 'fDep2.dat', 'fDep3.dat'],
    fAPP='fAPP.dat',
    fAPR='fAPR.dat',
    fHOSB='fHOSB.dat',
    fVOSB='fVOSB.dat',
    fEig='fEig.dat',
    fHW='fHW.dat',
    fVX='fVW.dat',
    fPT='fPT.dat'
)
#############################################################################################################
# Actual routine call DO NOT CHANGE ANYTHING BELOW THIS!
in_opts = dict()
in_opts.update(in_switches)
in_opts.update(in_parameters)
params = dict(
    run_opts=run_opts,
    pin_opts=pin_opts,
    hin_opts=hin_opts,
    in_opts=in_opts,
    in_file_names=in_file_names,
    mol=mol,
    dirs=dirs
)
Triatomic.MakeFiles.mka3(params)
