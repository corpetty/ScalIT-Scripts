__author__ = 'coreypetty'
# !/bin/env python
#
# generate .sh script files for queue system
#
import posix
from Util import setEnvironment


def get_sh_header(params):
    """
    get the header of script files for various HPC platforms.
    """
    # Lonestar at UT Texas at Austin - 13 March 2015
    if params['dirs']['host'] == 'Lonestar':
        header = '#!/bin/bash\n\n' \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + params['mol']["Name"] + "'\n\n"
    # Hrothgar cluster at TTU - 13 March 2015
    # NOTE: Please fill in number of desired cores from
    #       somewhere
    elif params['dirs']['host'] == 'Hrothgar':
        header = '#!/bin/bash                                       \n' \
                 + '#$ -V                                           \n' \
                 + '#$ -cwd                                         \n' \
                 + '#$ -j y                                         \n' \
                 + '#$ -R y                                         \n' \
                 + '#$ -S /bin/bash                                 \n' \
                 + "#$ -N '" + params['mol']["jtotal"] + params['mol']["Name"] \
                 + params['mol']["permutation"] + "'              \n" \
                 + '#$ -o $JOB_NAME.240.$JOB_ID.out                 \n' \
                 + '#$ -e $JOB_NAME.e$JOB_ID                        \n' \
                 + '#$ -q normal                                    \n' \
                 + '#$ -P hrothgar                                  \n' \
                 + '#$ -pe mpi ___                                  \n' \
                 + "BIN_DIR='" + params['dirs']["bin"] + params['mol']["Name"] + "'     \n" \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + "'\n         \n" \
                 + 'date'
    # Robinson Cluster at TTU Chemistry - 13 March 2015
    elif params['dirs']['host'] == 'Robinson':
        header = '#!/bin/bash                                       \n' \
                 + '#$ -V                                           \n' \
                 + '#$ -cwd                                         \n' \
                 + '#$ -j y                                         \n' \
                 + '#$ -R y                                         \n' \
                 + '#$ -S /bin/bash                                 \n' \
                 + "#$ -N '" + params['mol']["jtotal"] + params['mol']["Name"] \
                 + params['mol']["permutation"] + "'              \n" \
                 + '#$ -o $JOB_NAME.240.$JOB_ID.out                 \n' \
                 + '#$ -e $JOB_NAME.e$JOB_ID                        \n' \
                 + '#$ -q normal                                    \n' \
                 + '#$ -pe mpi 240                                  \n' \
                 + "BIN_DIR='" + params['dirs']["bin"] + params['mol']["Name"] + "'     \n" \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + "'\n         \n" \
                 + 'date'
    elif params['dirs']['host'] == 'local':
        header = "WK_DIR='" + params['dirs']["run_work_dir"] + "'\n\n"
    else:
        header = "## Create your own header ##"

    return header


def mkmsh(params):
    mpi = setEnvironment.environment_mpi(params)
    bin_dir = params['dirs']['bin'] + params['mol']['Name'] + '/'
    if params['run_opts']['version'] == 0:  # sequential program
        mpi['hin'] = bin_dir + params['mol']['Name'] + '_' + params['hin_opts']['permutation']
        mpi['in'] = params['dirs']['bin'] + 'iterate'
    elif params['run_opts']['version'] < 0:  # MPI 1
        mpi['hin'] = bin_dir + 'p' + params['mol']['Name'] + '_' + params['hin_opts']['permutation']
        mpi['in'] = params['dirs']['bin'] + 'p_iterate'
    else:  # MPI 2, Parallel IO
        mpi['hin'] = bin_dir + 'm' + params['mol']['Name'] + '_' + params['hin_opts']['permutation']
        mpi['in'] = params['dirs']['bin'] + 'm_iterate'

    sfile = params['dirs']['run_work_dir'] + params['mol']["Name"] + params['mol']['suffix'] + '.sh'
    fb0 = '$WK_DIR/' + params['mol']["Name"] + params['mol']['suffix']
    header = get_sh_header(params)
    fh = open(sfile, 'w')
    fh.write(header)
    for x in params['run_opts']['nvar']:
        fb = '%(fb)s_%(x)d' % {'fb': fb0, 'x': x}
        fhin = fb + '.hin'
        fhout = fb + '.hout'
        fin = fb + '.in'
        fout = fb + '.out'
        fh.write('(')
        fh.write(mpi['cmd'] + ' ' + mpi['hin'] + ' <  ' + fhin + ' >  ' + fhout + '\n')
        fh.write(mpi['cmd'] + ' ' + mpi['in'] + ' <  ' + fin + ' >  ' + fout + '\n')
        fh.write(') &\n\n')
    fh.close()
    posix.system('chmod u+x ' + sfile)
    print '    File Generated: ' + sfile
