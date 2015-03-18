__author__ = 'Corey Petty'


def environment_mpi(params):
    """
    Sets the MPI environment variables
    :param params: 
    :return mpi: dictionary of MPI environment variables
    """
    # TODO: incorporate the "mpi" variable into the params Dictionary
    mpi = {}
    
    if params['run_opts']['version'] == 0:  # Sequential program
        mpi['cmd'] = ''
    elif params['dirs']['host'] == 'Hrothgar':  # options in hrothgar cluster
        mpi['cores_per_node'] = 12
        mpi['cores'] = mpi['cores_per_node'] * params['run_opts']['nodes_desired']
        mpi['cmd'] = 'mpirun -np %(np)d -machinefile machinefile.$JOB_ID' % {'np': mpi['cores']}
    elif params['dirs']['host'] == 'Robinson':
        mpi['cores_per_node'] = 12
        mpi['cores'] = mpi['cores_per_node'] * params['run_opts']['nodes_desired']
        mpi['cmd'] = 'mpirun -np %(np)d -machinefile machinefile.$JOB_ID' % {'np': mpi['cores']}
    elif params['dirs']['host'] == 'Lonestar':
        mpi['cores_per_node'] = 12
        mpi['cores'] = mpi['cores_per_node'] * params['run_opts']['nodes_desired']
        mpi['cmd'] = 'ibrun -n %(np)d -o 0' % {'np': mpi['cores']}
    elif params['dirs']['host'] == 'local':
        mpi['cores'] = params['run_opts']['local_cores']
        mpi['cmd'] = 'mpirun -np %(np)d' % {'np': mpi['cores']}
    
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

    return mpi