__author__ = 'Corey Petty'
import os
import stat


#  TODO:  Add bash script generator to submit all jobs SGE submissions
def set_submission_header(molecule, platform, directories):
    if platform.submission_type == 'sge':
        platform.submission_header = [
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
            % {'cores': platform.cores},
            '#$ -e $JOB_NAME.e$JOB_ID\n'
        ]
    elif platform.submission_type == 'pbs':
        platform.submission_header = [
            '# !/bin/bash\n',
            '# PBS -S /bin/bash\n',
            '#\n',
            '## nodes = requested nodes\n',
            '## ppn = cores per node\n',
            '# PBS -l nodes={}:ppn=20\n'.format(
                platform.nodes_desired
            ),
            '#\n',
            '## Por default deixar node-exclusive\n',
            '# PBS -n node-exclusive\n',
            '#\n',
            '## Choose a queue:\n',
            '## "oldnodes" 5x(8 cores 24 Gb RAM)\n',
            '## "newnodes" 6x(20 cores 128 Gb RAM), definir abaixo.\n',
            '# PBS -q newnodes\n',
            '#\n',
            '# PBS -l walltime={}\n'.format(
                platform.runtime
            ),
            '#\n',
            '## Set your email for job cancel/finish.\n',
            '## PBS -m ae\n',
            '## PBS -M <email here>\n',
            '#\n',
            "## Jobname, shows on 'qstat'.\n",
            '# PBS -N ScalIT\n',
            '\n',
            "echo -e \"\\n## Job iniciado em $(date +'%d-%m-%Y as %T') #####################\\n\"\n",
            '## Bin directory of ScalIT\n',
            'BINDIR={}\n'.format(directories.bin),
            '\n',
            '## Variavel com o diretorio de scratch do job\n',
            "SCRWRKDIR=$SCRATCH/$PBS_JOBNAME\n",
            '## O nome dos arquivos de input e output sao baseados no\n',
            '## nome do job (linha "#PBS -N xxx" acima).\n',
            '## Observe que nao e obrigatorio esta forma de nomear os arquivos.\n',
            "INP=$PBS_JOBNAME.com\n",
            "OUT=$PBS_JOBNAME.out\n",
            '\n',
            '## O diretorio onde o job sera executado sera apagado, por padrao, ao\n',
            '## final do mesmo.\n',
            '## Se desejar que nao seja apagado, substitua Y por N.\n',
            'APAGA_SCRATCH = Y\n',
            '\n',
            '## Informacoes do job impressos no arquivo de saida.\n',
            "echo -e\"\n## Jobs ativos de $USER: \n\"\n",
            "qstat -an -u $USER",
            "echo -e \"\n## Node de execucao do job:         $(hostname -s) \n\"\n",
            "echo -e \"\n## Numero de tarefas para este job: $PBS_TASKNUM \n\"\n",
            '\n',
            '#########################################\n',
            '##-------  Inicio do trabalho     ----- #\n',
            '#########################################\n',
            '\n',
            '## descarregar todos os modulos\n',
            'module purge\n',
            '\n',
            '## Configura o ambiente de execucao do software.\n',
            'module load runtime/intel/16.0\n',
            'module load compilers/intel/16.0\n',
            'module load libraries/ipmi/5.1\n',
            'module load libraries/mkl/16.0\n',
            '\n',

        ]
    elif platform.submission_type == 'slurm':
        platform.submission_header = [
            '#!/bin/bash\n',
            '#----------------------------------------------------\n',
            '# SLURM job script to run MPI applications\n',
            '#----------------------------------------------------\n',
            '#SBATCH -J J%(j_total)d%(mol)s_%(perm)s\n'
            % {'j_total': molecule.j_total,
               'mol': molecule.name,
               'perm': molecule.permutation
               },
            '#SBATCH -o $SLURM_JOB_NAME.{}.o%j   # Name of stdout output file\n'.format(
                platform.cores
            ),
            '#SBATCH -e mpi_job.o%j         # Name of stdout output file\n',
            '#SBATCH -N {}                   # Total number of nodes requested\n'.format(
                platform.nodes_desired
            ),
            '#SBATCH -n {}                  # Total number of mpi tasks requested\n'.format(
                platform.cores
            ),
            '#SBATCH -t {}            # Run time (hh:mm:ss) - 1.5 hours\n'.format(
                platform.runtime
            ),
        ]
    else:
        platform.submission_header = []


def set_submission_footer(molecule, platform):
    if platform.submission_type == 'pbs':
        platform.submission_footer = [
            '\n',
            "## Copia o diretorio de scratch para o diretorio original do job.\n",
            "cp -r $OUTPUT $PBS_O_WORKDIR/\n",
            '\n',
            "## Apaga o diretorio de scratch do job.\n",
            "if [ x\"$APAGA_SCRATCH\" = x\"Y\" ]; then\n",
            "\trm -rf $SCRWRKDIR\n",
            'else\n',
            "\techo -e \"\\nO diretorio \\e[00;31m$WRKDIR\\e[00m deve ser removido manualmente\"\n",
            "\techo -e \"para evitar problemas para outros jobs e/ou usuarios. \\n\"\n",
            'fi\n',
            '\n',
            "echo -e \"\\n## Job finalizado em $(date +'%d-%m-%Y as %T') ###################\"\n",
        ]
    else:
        platform.submission_footer = []


def get_executables(molecule, platform):
    if platform.use_mpi:
        if molecule.permutation == 'even':
            platform.hin_exec = 'p%(name)s_e' % {'name': molecule.name}
        else:
            platform.hin_exec = 'p%(name)s_o' % {'name': molecule.name}
        platform.in_exec = 'p_iterate'
    else:
        if molecule.permutation == 'even':
            platform.hin_exec = '%(name)s_e' % {'name': molecule.name}
        else:
            platform.hin_exec = '%(name)s_o' % {'name': molecule.name}
        platform.in_exec = 'iterate'


def run_script(directories, files, molecule, platform, options):
    get_executables(molecule=molecule, platform=platform)

    #  Open file for writing
    fh = open(directories.run + '/' + files.run_script, 'w')

    #  Get submission engine header for platform if necessary
    #  OLD
    # set_header(molecule=molecule, mpi=mpi)
    set_submission_header(molecule=molecule, platform=platform, directories=directories)
    fh.write("".join(platform.submission_header))
    fh.write("".join(platform.submission_appendeges))

    #  Write remaining part of the file
    fh.write('BIN_DIR=%(bin_dir)s\n' % {'bin_dir': directories.bin})
    fh.write('WK_DIR=%(run_dir)s\n\n' % {'run_dir': directories.run})
    fh.write('date\n')
    fh.write('( \n')

    if (options.run_switch == 1) or (options.run_switch == 3):
        fh.write('%(hinmpi)s $BIN_DIR/%(name)s/%(exec)s < $WK_DIR/%(input)s > $WK_DIR/%(output)s\n'
                 % {'hinmpi': platform.mpi_hin_cmd,
                    'name': molecule.name,
                    'exec': platform.hin_exec,
                    'input': files.hamiltonian + files.input,
                    'output': files.hamiltonian + files.output
                    }
                 )
    if (options.run_switch == 2) or (options.run_switch == 3):
        fh.write('%(mpi)s $BIN_DIR/%(exec)s < $WK_DIR/%(input)s > $WK_DIR/%(output)s\n'
                 % {'mpi': platform.mpi_cmd,
                    'name': molecule.name,
                    'exec': platform.in_exec,
                    'input': files.iterate + files.input,
                    'output': files.iterate + files.output
                    }
                 )
    fh.write(')& \n')
    fh.write('wait\n')
    fh.write('date')
    set_submission_footer(molecule=molecule, platform=platform)
    fh.write("".join(platform.submission_footer))
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
