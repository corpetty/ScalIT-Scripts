__author__ = 'Corey Petty'
# !/bin/env python
import posix
from Util import setEnvironment


def mkmsh(params, variable):
    header = get_sh_header(params, variable)

    sfile = params['dirs']['run_work_dir'] + '/' + params['mol']["Name"] + params['mol']['suffix'] \
            + '_' + str(variable) + '.sh'
    fb0 = '$WK_DIR/' + params['mol']["Name"] + params['mol']['suffix']
    fh = open(sfile, 'w')
    fh.write(header)
    fb = '%(fb)s_%(x)d' % {'fb': fb0, 'x': variable}
    fhin = fb + '.hin'
    fhout = fb + '.hout'
    fin = fb + '.in'
    fout = fb + '.out'
    fh.write('(')
    fh.write(params['mpi']['cmd'] + ' ' + params['mpi']['hin'] + ' <  ' + fhin + ' >  ' + fhout + '\n')
    fh.write(params['mpi']['cmd'] + ' ' + params['mpi']['in'] + ' <  ' + fin + ' >  ' + fout + '\n')
    fh.write(') &\n\n')
    fh.write('wait \n')
    if params['dirs']['host'] == 'Robinson' or params['dirs']['host'] == 'Lonestar':
        fh.write('rm machinefile.$JOB_ID \n')
    fh.write('date')
    fh.close()
    posix.system('chmod u+x ' + sfile)
    print '    File Generated: ' + sfile


def get_sh_header(params, variable):
    """
    get the header of script files for various HPC platforms.
    :returns: str
    """
    # Lonestar at UT Texas at Austin - 13 March 2015
    setEnvironment.environment_mpi(params)
    if params['dirs']['host'] == 'Lonestar':
        header = '#!/bin/bash                                                   \n' \
                 + '#$ -V                                                       \n' \
                 + '#$ -cwd                                                     \n' \
                 + '#$ -j y                                                     \n' \
                 + '#$ -R y                                                     \n' \
                 + '#$ -S /bin/bash                                             \n' \
                 + '#$ -l h_rt=' + params['run_opts']['run_time'] + '           \n' \
                 + "#$ -N '" + str(params['hin_opts']["j_total"]) + params['mol']["Name"] \
                 + params['hin_opts']["permutation"] + "'                       \n" \
                 + '#$ -o $JOB_NAME.' + str(params['mpi']['cores'])                 \
                 + '.$JOB_ID                                                    \n' \
                 + '#$ -e $JOB_NAME.e$JOB_ID                                    \n' \
                 + '#$ -q normal                                                \n' \
                 + '#$ -pe 12way ' + str(params['mpi']['cores']) + '            \n' \
                 + "BIN_DIR='" + params['dirs']["bin"] + "'                     \n" \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + "'           \n\n" \
                 + 'date \n'
    # Hrothgar cluster at TTU - 13 March 2015
    elif params['dirs']['host'] == 'Hrothgar':
        header = '#!/bin/bash                                                   \n' \
                 + '#$ -V                                                       \n' \
                 + '#$ -cwd                                                     \n' \
                 + '#$ -j y                                                     \n' \
                 + '#$ -R y                                                     \n' \
                 + '#$ -S /bin/bash                                             \n' \
                 + "#$ -N '" + params['hin_opts']["j_total"] + params['mol']["Name"] \
                 + params['hin_opts']["permutation"] + "'                       \n" \
                 + '#$ -o $JOB_NAME.' + str(params['mpi']['cores'])                 \
                 + '.$JOB_ID                                                    \n' \
                 + '#$ -e $JOB_NAME.e$JOB_ID                                    \n' \
                 + '#$ -q normal                                                \n' \
                 + '#$ -P hrothgar                                              \n' \
                 + '#$ -pe mpi ' + str(params['mpi']['cores']) + '              \n' \
                 + "BIN_DIR='" + params['dirs']["bin"] + "'                     \n" \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + "'           \n\n" \
                 + 'date \n'
    # Robinson Cluster at TTU Chemistry - 13 March 2015
    elif params['dirs']['host'] == 'Robinson':
        header = '#!/bin/bash                                        \n' \
                 + '#$ -V                                            \n' \
                 + '#$ -cwd                                          \n' \
                 + '#$ -j y                                          \n' \
                 + '#$ -R y                                          \n' \
                 + '#$ -S /bin/bash                                  \n' \
                 + "#$ -N J" + str(params['hin_opts']["j_total"])         \
                 + params['mol']["Name"]                                 \
                 + '_' + params['hin_opts']["permutation"] + "       \n" \
                 + '#$ -o $JOB_NAME.' + str(params['mpi']['cores'])      \
                 + '.$JOB_ID.out                                     \n' \
                 + '#$ -e $JOB_NAME.e$JOB_ID                         \n' \
                 + '#$ -q normal.q                                      \n' \
                 + '#$ -pe mpi ' + str(params['mpi']['cores']) + '   \n' \
                 + "BIN_DIR='" + params['dirs']["bin"] + "'          \n" \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + "'\n\n" \
                 + 'date\n'
    elif params['dirs']['host'] == 'local':
        header = '#!/bin/bash                                        \n' \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + "'  \n" \
                 + "BIN_DIR='" + params['dirs']["bin"] + "'      \n  \n" \
                 + 'date \n'
    else:
        header = "#!/bin/bash                                         \n" \
                 + '## Create your own header ##                      \n' \
                 + "BIN_DIR='" + params['dirs']['bin'] + "'           \n" \
                 + "WK_DIR='" + params['dirs']["run_work_dir"] + "' \n\n" \
                 + 'date \n'

    return header
