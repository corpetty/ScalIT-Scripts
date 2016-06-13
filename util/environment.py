__author__ = 'Corey Petty'


class Directories(object):
    """
    Class object that simply holds all relavent ScalIT directory locations
    """
    def __init__(self, work="work", data="data", scalit="ScalIT"):
        self.work = work
        self.data = data
        self.scalit = scalit
        self.check_for_slash()

    def check_for_slash(self):
        if self.data[-1] == '/':
            self.data = self.data[:-1]
        if self.work[-1] == '/':
            self.work = self.work[:-1]
        if self.scalit[-1] == '/':
            self.scalit = self.scalit[:-1]


class Files(object):
    def __init__(self):
        self.psovbr_lr = None

    pass


class Mpi(object):  # Deprecated
    def __init__(self,
                 use_mpi=True, use_sge=True, platform='local', nodes_desired=1, cores=1, runtime='48:00:00',
                 project=''):
        self.use_mpi = use_mpi
        self.use_sge = use_sge
        self.platform = platform
        self.nodes_desired = nodes_desired
        self.cores = cores
        self.cmd = 'mpirun -np %(np)d ' % {'np': self.cores}
        self.cmdhin = 'mpirun -np %(np)d ' % {'np': self.cores}
        self.cores_per_node = 1
        self.runtime = runtime
        self.header = ''
        self.submission_appendeges = ''
        self.project = project
        self.set_platform_specifics()

    def set_platform_specifics(self):
        if not self.use_mpi:
            self.cmd = ''
            self.cmdhin = ''
            self.cores = 1
        elif self.platform == 'local':
            self.cmd = 'mpirun -np %(np)d ' \
                       % {'np': self.cores}
            self.cmdhin = 'mpirun -np %(np)d ' \
                          % {'np': self.cores}
        elif self.platform == 'Robinson':
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.cmd = "mpirun -np %(np)d -machinefile machinefile.$JOB_ID " \
                       % {'np': self.cores}
            self.cmdhin = "mpirun -np 4 -machinefile machinefile.$JOB_ID "
        elif self.platform == 'Lonestar4':
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.cmd = 'ibrun -n %(cores)d -o 0 ' \
                       % {'cores': self.cores}
            self.cmdhin = 'ibrun -n 4 -o 0 '
            self.use_mpi = True
            self.use_sge = True
            self.submission_appendeges = '#$ -l h_rt=' + self.runtime + '\n'
        elif self.platform == 'Hrothgar':
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.cmd = "mpirun -np %(np)d -machinefile machinefile.$JOB_ID " \
                       % {'np': self.cores}
            self.cmdhin = "mpirun -np 4 -machinefile machinefile.$JOB_ID "
        elif self.platform == 'Lonestar5':
            self.cores_per_node = 24
            self.cores = self.cores_per_node * self.nodes_desired
            self.cmd = 'ibrun tacc_affinity ' \
                       % {'cores': self.cores}
            self.cmdhin = "ibrun -n {} -o 0 tacc_affinity ".format(self.cores_per_node)
            self.submission_appendeges = [
                '#SBATCH -A {}      # <-- Allocation name to charge job against\n'.format(self.project),
            ]


class Platform(object):
    def __init__(self, platform='', submission_type='', submission_header='', submission_appendeges='',
                 use_mpi=True, mpi_cmd='mpirun', mpi_hin_cmd='mpirun', cores_per_node=12, nodes_desired=1, cores=1,
                 runtime='48:00:00', project='', submission_footer=''):
        self.platform = platform
        self.submission_type = submission_type
        self.submission_header = submission_header
        self.submission_footer = submission_footer
        self.nodes_desired = nodes_desired
        self.cores_per_node = cores_per_node
        self.cores = cores
        self.use_mpi = use_mpi
        self.mpi_cmd = mpi_cmd
        self.mpi_hin_cmd = mpi_hin_cmd
        self.runtime = runtime
        self.project = project
        self.submission_appendeges = submission_appendeges
        self.set_platform_specifics()

    def set_platform_specifics(self):
        if not self.use_mpi:
            self.mpi_cmd = ''
            self.mpi_hin_cmd = ''
            self.cores = 1
        elif self.platform == 'local':
            self.mpi_cmd = 'mpirun -np %(np)d ' \
                       % {'np': self.cores}
            self.mpi_hin_cmd = 'mpirun -np %(np)d ' \
                          % {'np': self.cores}
        elif self.platform == 'Robinson':
            self.submission_type = 'sge'
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.mpi_cmd = "mpirun -np %(np)d -machinefile machinefile.$JOB_ID " \
                       % {'np': self.cores}
            self.mpi_hin_cmd = "mpirun -np 4 -machinefile machinefile.$JOB_ID "
            self.submission_appendeges = [
                '#$ -q normal.q\n',
                '#$ -pe mpi {}\n'.format(self.cores),
                '\n'
            ]
        elif self.platform == 'Lonestar4':
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.mpi_cmd = 'ibrun -n %(cores)d -o 0 ' \
                       % {'cores': self.cores}
            self.mpi_hin_cmd = 'ibrun -n 4 -o 0 '
            self.use_mpi = True
            self.submission_type = 'sge'
            self.submission_appendeges = '#$ -l h_rt=' + self.runtime + '\n'
        elif self.platform == 'Hrothgar':
            self.submission_type = 'sge'
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.mpi_cmd = "mpirun -np %(np)d -machinefile machinefile.$JOB_ID " \
                       % {'np': self.cores}
            self.mpi_hin_cmd = "mpirun -np 4 -machinefile machinefile.$JOB_ID "
            self.submission_appendeges = [
                '#$ -q normal\n',
                '#$ -P hrothgar\n',
                '#$ -pe mpi {}\n'.format(self.cores),
                '\n'
            ]
        elif self.platform == 'Lonestar5':
            self.cores_per_node = 24
            self.cores = self.cores_per_node * self.nodes_desired
            self.mpi_cmd = 'ibrun tacc_affinity ' \
                       % {'cores': self.cores}
            self.mpi_hin_cmd = "ibrun tacc_affinity "
            self.submission_type = 'slurm'
            self.submission_appendeges = [
                '#SBATCH -A {}              # <-- Allocation name to charge job against\n'.format(self.project),
                '#SBATCH -p normal              # Queue name\n',
                '\n'
            ]
        elif self.platform == "Eter":
            self.cores_per_node = 20
            self.cores = self.cores_per_node * self.nodes_desired
            self.mpi_cmd = 'mpirun -np $PBS_NP'
            self.mpi_hin_cmd = 'mpirun -np $PBS_NP'
            self.submission_type = 'pbs'
            self.submission_appendeges = [
                '\n'
            ]