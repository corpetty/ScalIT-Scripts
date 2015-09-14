__author__ = 'Corey Petty'

import posixpath
import os


def set_default_directories(params):
    """
    Routine to set up default directories from user inputed directories
    :param params: Dictionary of all run parameters
    :type params: dict
    :return: null
    """
    params['dirs']['bin'] = params['dirs']['scalit'] + '/' + 'bin'
    params['dirs']['pes'] = params['dirs']['scalit'] + '/' + 'src/systems'
    params['dirs']['pes_data'] = params['dirs']['scalit'] + '/' + 'data'

    # Setting the directory script/input/output files will be stored for runs (usually $WORK space)
    params['dirs']['work_mol_dir'] = params['dirs']['work'] + '/' + params['mol']['Name']
    if params['mol']['mass_opt'] == '':
        params['dirs']['run_dir'] = params['dirs']['work_mol_dir']
    else:
        params['dirs']['run_dir'] = params['dirs']['work_mol_dir'] + '/' + params['mol']['mass_opt']
    if params['hin_opts']['permutation'] == 'e':
        params['dirs']['run_dir'] += '/even'
    else:
        params['dirs']['run_dir'] += '/odd'
    params['dirs']['run_dir'] += '/' + params['mol']['suffix']

    # Setting the directory data files will be stored for jobs (usually $SCRATCH space)
    params['dirs']['data_mol_dir'] = params['dirs']['data'] + '/' + params['mol']['Name']
    if params['mol']['mass_opt'] == '':
        params['dirs']['run_data_dir'] = params['dirs']['data_mol_dir']
    else:
        params['dirs']['run_data_dir'] = params['dirs']['data_mol_dir'] + '/' + params['mol']['mass_opt']
    if params['hin_opts']['permutation'] == 'e':
        params['dirs']['run_data_dir'] += '/even'
    else:
        params['dirs']['run_data_dir'] += '/odd'


    if params['mol']['mass_opt'] == '':
        params['dirs']['psovbr_dir'] = params['dirs']['data_mol_dir']
    else:
        params['dirs']['psovbr_dir'] = params['dirs']['data_mol_dir'] + '/' + params['mol']['mass_opt']
    params['dirs']['psovbr_dir'] += '/psovbr'


    print '----> Checking for directory existence'

    if not posixpath.exists(params['dirs']['work']):
        print '    Creating: ' + params['dirs']['work']
        os.makedirs(params['dirs']['work'])
    else:
        print '    Directory Exists: ' + params['dirs']['work']

    if not posixpath.exists(params['dirs']['run_dir']):
        print '    Creating: ' + params['dirs']['run_dir']
        os.makedirs(params['dirs']['run_dir'])
    else:
        print '    Directory Exists: ' + params['dirs']['run_dir']

    if not posixpath.exists(params['dirs']['data']):
        print '    Creating: ' + params['dirs']['data']
        os.makedirs(params['dirs']['data'])
    else:
        print '    Directory Exists: ' + params['dirs']['data']

    if not posixpath.exists(params['dirs']['run_data_dir']):
        print '    Creating: ' + params['dirs']['run_data_dir']
        os.makedirs(params['dirs']['run_data_dir'])
    else:
        print '    Directory Exists: ' + params['dirs']['run_data_dir']

    if params['mol']['suffix'] == 'p':

        # Setting the psovbr data directory
        if not posixpath.exists(params['dirs']['psovbr_dir']):
            print '    Creating: ' + params['dirs']['psovbr_dir']
            os.makedirs(params['dirs']['psovbr_dir'])
        else:
            print '    Directory Exists: ' + params['dirs']['psovbr_dir']
