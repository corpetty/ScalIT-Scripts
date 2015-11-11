__author__ = 'Corey Petty'
import os
import stat


def set_header(molecule, mpi):
    #  TODO: Add Lonestar, Hrothgar header specifics
    if mpi.use_sge:
        mpi.header = [
            '#!/bin/bash\n',
            '#$ -V\n',
            '#$ -cwd\n',
            '#$ -j y\n',
            '#$ -R y\n',
            '#$ -S /bin/bash\n',
            '#$ -N J%(j_total)d%(mol)s_%(perm)s\n'
            % {'j_total': molecule.j_total,
               'mol': molecule.name,
               'perm': molecule.permutation
               },
            '#$ -o $JOB_NAME.%(cores)d.$JOB_ID.o\n'
            % {'cores': mpi.cores},
            '#$ -e $JOB_NAME.e$JOB_ID\n'
        ]
        if mpi.platform == 'Robinson':
            mpi.header.append('#$ -q normal.q\n')
            mpi.header.append('#$ -pe mpi %(cores)d\n\n' % {'cores': mpi.cores})
    else:
        mpi.header = []


def get_executables(molecule, mpi):
    if mpi.use_mpi:
        if molecule.permutation:
            mpi.hin_exec = 'p%(name)s_o' % {'name': molecule.name}
        else:
            mpi.hin_exec = 'p%(name)s_e' % {'name': molecule.name}
        mpi.in_exec = 'p_iterate'
    else:
        if molecule.permutation:
            mpi.hin_exec = '%(name)s_o' % {'name': molecule.name}
        else:
            mpi.hin_exec = '%(name)s_e' % {'name': molecule.name}
        mpi.in_exec = 'iterate'


def run_script(directories, files, molecule, mpi):
    get_executables(molecule=molecule, mpi=mpi)

    #  Open file for writing
    fh = open(directories.run + '/' + files.run_script, 'w')

    #  Get SGE submission engine header for platform
    if mpi.use_sge:
        set_header(molecule=molecule, mpi=mpi)

        fh.write("".join(mpi.header))

    #  Write remaining part of the file
    fh.write('BIN_DIR=%(bin_dir)s\n' % {'bin_dir': directories.bin})
    fh.write('WK_DIR=%(run_dir)s\n\n' % {'run_dir': directories.run})
    fh.write('date\n')
    fh.write('( \n')
    fh.write('%(hinmpi)s $BIN_DIR/%(name)s/%(exec)s < $WK_DIR/%(input)s\n'
             % {'hinmpi': mpi.cmdhin,
                'name': molecule.name,
                'exec': mpi.hin_exec,
                'input': files.hamiltonian + files.input
                }
             )
    fh.write('%(mpi)s $BIN_DIR/%(name)s/%(exec)s < $WK_DIR/%(input)s\n'
             % {'mpi': mpi.cmd,
                'name': molecule.name,
                'exec': mpi.in_exec,
                'input': files.iterate + files.input
                }
             )
    fh.write(')& \n')
    fh.write('wait\n')
    fh.write('date')
    fh.close()
    print('    File Generated: ' + directories.run + '/' + files.run_script)


def pin_script(directories, files, molecule):
    #  Open file for writing
    fh = open(directories.run_psovbr + '/' + files.run_psovbr_script, 'w')

    #  Write the file
    fh.write('#!/usr/bin/env bash\n')
    fh.write('BIN_DIR=%(bin_dir)s\n' % {'bin_dir': directories.bin})
    fh.write('WK_DIR=%(run_dir)s\n\n' % {'run_dir': directories.run_psovbr})
    fh.write('date\n')
    fh.write('$BIN_DIR/%(name)s/%(exec_lr)s < $WK_DIR/%(input)s > $WK_DIR/%(output)s &\n'
             % {'name': molecule.name,
                'exec_lr': molecule.name + 'vlr',
                'input': files.presinc_lr + files.input,
                'output': files.presinc_lr + files.output
                }
             )
    fh.write('$BIN_DIR/%(name)s/%(exec_br)s < $WK_DIR/%(input)s > $WK_DIR/%(output)s &\n'
             % {'name': molecule.name,
                'exec_br': molecule.name + 'vBR',
                'input': files.presinc_br + files.input,
                'output': files.presinc_br + files.output
                }
             )
    fh.write('wait\n')
    fh.write('date')
    fh.close()
    st = os.stat(directories.run_psovbr + '/' + files.run_psovbr_script)
    os.chmod(directories.run_psovbr + '/' + files.run_psovbr_script, st.st_mode | stat.S_IEXEC)
    print('    File Generated: ' + directories.run_psovbr + '/' + files.run_psovbr_script)
