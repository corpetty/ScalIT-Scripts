__author__ = 'coreypetty'
# !/bin/env python
#
# generate .sh script files for queue system
#
import posix


def get_sh_header(mol, dirs):
    """
    get the header of script files for various HPC platforms.
    """
    # Lonestar at UT Texas at Austin - 13 March 2015
    if dirs['host'] == 'Lonestar':
        header = '#!/bin/bash\n\n' \
                 + "WK_DIR='" + dirs["work"] + mol["Name"] + "'\n\n"
    # Hrothgar cluster at TTU - 13 March 2015
    # NOTE: Please fill in number of desired cores from
    #       somewhere
    elif dirs['host'] == 'Hrothgar':
        header = '#!/bin/bash                                       \n' \
                 + '#$ -V                                           \n' \
                 + '#$ -cwd                                         \n' \
                 + '#$ -j y                                         \n' \
                 + '#$ -R y                                         \n' \
                 + '#$ -S /bin/bash                                 \n' \
                 + "#$ -N '" + mol["jtotal"] + mol["Name"] \
                 + mol["permutation"] + "'              \n" \
                 + '#$ -o $JOB_NAME.240.$JOB_ID.out                 \n' \
                 + '#$ -e $JOB_NAME.e$JOB_ID                        \n' \
                 + '#$ -q normal                                    \n' \
                 + '#$ -P hrothgar                                  \n' \
                 + '#$ -pe mpi ___                                  \n' \
                 + "BIN_DIR='" + dirs["bin"] + mol["Name"] + "'     \n" \
                 + "WK_DIR='" + dirs["work"] + mol["Name"] + "'\n   \n" \
                 + 'date'
    # Robinson Cluster at TTU Chemistry - 13 March 2015
    elif dirs['host'] == 'Robinson':
        header = '#!/bin/bash                                     \n' \
                 + '#$ -V                                           \n' \
                 + '#$ -cwd                                         \n' \
                 + '#$ -j y                                         \n' \
                 + '#$ -R y                                         \n' \
                 + '#$ -S /bin/bash                                 \n' \
                 + "#$ -N '" + mol["jtotal"] + mol["Name"] \
                 + mol["permutation"] + "'              \n" \
                 + '#$ -o $JOB_NAME.240.$JOB_ID.out                 \n' \
                 + '#$ -e $JOB_NAME.e$JOB_ID                        \n' \
                 + '#$ -q normal                                    \n' \
                 + '#$ -pe mpi 240                                  \n' \
                 + "BIN_DIR='" + dirs["bin"] + mol["Name"] + "'     \n" \
                 + "WK_DIR='" + dirs["work"] + mol["Name"] + "'\n   \n" \
                 + 'date'
    elif dirs['host'] == 'PettyMBP':
        header = "WK_DIR='" + dirs["work"] + mol["Name"] + "'\n\n"
    else:
        header = "## Create your own header ##"

    return header


def mkmsh(cmd, mol, dirs, n0):
    sfile = dirs["work"] + mol["Name"] + '/' + mol["Name"] + mol['suffix'] + '.sh'
    fb0 = '$WK_DIR/' + mol["Name"] + mol['suffix']
    header = get_sh_header(mol, dirs)
    fh = open(sfile, 'w')
    fh.write(header)
    for x in n0:
        fb = '%(fb)s_%(x)d' % {'fb': fb0, 'x': x}
        fhin = fb + '.hin'
        fhout = fb + '.hout'
        fin = fb + '.in'
        fout = fb + '.out'
        fh.write('(')
        fh.write(cmd['mpi'] + ' ' + cmd['hin'] + ' <  ' + fhin + ' >  ' + fhout + '\n')
        fh.write(cmd['mpi'] + ' ' + cmd['in'] + ' <  ' + fin + ' >  ' + fout + '\n')
        fh.write(') &\n\n')
    fh.close()
    posix.system('chmod u+x ' + sfile)
