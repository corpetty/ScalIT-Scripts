__author__ = 'Corey Petty'


class Directories(object):
    """
    Class object that simply holds all relavent ScalIT directory locations
    """
    def __init__(self, work="work", data="data", scalit="ScalIT"):
        self.work = work
        self.data = data
        self.scalit = scalit


class Files(object):
    def __init__(self):
        self.psovbr_lr = None

    pass


class Mpi(object):
    def __init__(self,
                 use_mpi=True, use_sge=False, platform='local', nodes_desired=1, cores=1, runtime='48:00:00'):
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
        self.appendeges = ''
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
            self.appendeges = '#$ -l h_rt=' + self.runtime + '\n'
        elif self.platform == 'Hrothgar':
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.cmd = "mpirun -np %(np)d -machinefile machinefile.$JOB_ID " \
                       % {'np': self.cores}
            self.cmdhin = "mpirun -np 4 -machinefile machinefile.$JOB_ID "
        elif self.platform == 'Lonestar5':
            self.cores_per_node = 12
            self.cores = self.cores_per_node * self.nodes_desired
            self.cmd = 'ibrun -n %(cores) -o 0 ' \
                       % {'cores': self.cores}
