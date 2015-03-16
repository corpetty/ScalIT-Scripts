__author__ = 'Corey Petty'


def environment_mpi(dirs, mol, run_options):
    """
    Sets the MPI environment based on mol, directory, and platform
    :param dirs: Includes pertinant directories and platform
    :param mol: Includes molecular system parameters
    :return mpi: dictionary of MPI environment variables
    """
    mpi = {}
    
    if run_options['version'] == 0:  # Sequential program
        mpi['cmd'] = ''
    elif dirs['host'] == 'Hrothgar':  # options in hrothgar cluster
        mpi['cores_per_node'] = 12
        mpi['cores'] = mpi['cores_per_node'] * run_options['nodes_desired']
        mpi['cmd'] = 'mpirun -np %(np)d -machinefile machinefile.$JOB_ID' % {'np': mpi['cores']}
    elif dirs['host'] == 'Robinson':
        mpi['cores_per_node'] = 12
        mpi['cores'] = mpi['cores_per_node'] * run_options['nodes_desired']
        mpi['cmd'] = 'mpirun -np %(np)d -machinefile machinefile.$JOB_ID' % {'np': mpi['cores']}
    elif dirs['host'] == 'Lonestar':
        mpi['cores_per_node'] = 12
        mpi['cores'] = mpi['cores_per_node'] * run_options['nodes_desired']
        mpi['cmd'] = 'ibrun -n %(np)d -o 0' % {'np': mpi['cores']}
    elif dirs['host'] == 'local':
        mpi['cores'] = run_options['local_cores']
        mpi['cmd'] = 'mpirun -np %(np)d' % {'np': mpi['cores']}
    
    bin_dir = dirs['bin'] + mol['Name'] + '/'
    if run_options['version'] == 0:  # sequential program
        mpi['hin'] = bin_dir + mol['Name'] + '_' + mol['permutation']
        mpi['in'] = dirs['bin'] + 'iterate'
    elif run_options['version'] < 0:  # MPI 1
        mpi['hin'] = bin_dir + 'p' + mol['Name'] + '_' + mol['permutation']
        mpi['in'] = dirs['bin'] + 'p_iterate'
    else:  # MPI 2, Parallel IO
        mpi['hin'] = bin_dir + 'm' + mol['Name'] + '_' + mol['permutation']
        mpi['in'] = dirs['bin'] + 'm_iterate'

    return mpi