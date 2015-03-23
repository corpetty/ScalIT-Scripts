__author__ = 'Corey Petty'


def environment_mpi(params):
    """
    Sets the MPI environment variables, add to the params Dictionary
    :param params: 
    :return: null
    """
    mpi = {}
    
    if params['run_opts']['version'] == 0:  # Sequential program
        mpi['cmd'] = ''
        mpi['cores'] = 1
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

    if params['run_opts']['version'] == 0:  # sequential program
        mpi['hin'] = "$BIN_DIR/" + params['mol']['Name'] + '/' \
                     + params['mol']['Name'] + '_' + params['hin_opts']['permutation']
        mpi['in'] = "$BIN_DIR/" + 'iterate'
    elif params['run_opts']['version'] < 0:  # MPI 1
        mpi['hin'] = "$BIN_DIR/" + params['mol']['Name'] + '/' \
                     + 'p' + params['mol']['Name'] + '_' + params['hin_opts']['permutation']
        mpi['in'] = "$BIN_DIR/" + 'p_iterate'
    else:  # MPI 2, Parallel IO
        mpi['hin'] = "$BIN_DIR/" + params['mol']['Name'] + '/' \
                     + 'm' + params['mol']['Name'] + '_' + params['hin_opts']['permutation']
        mpi['in'] = "$BIN_DIR/" + 'm_iterate'

    params['mpi'] = mpi