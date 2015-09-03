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
    params['dirs']['run_work_dir'] = params['dirs']['work'] + '/' + params['mol']['Name'] + params['mol']['suffix']
    params['dirs']['run_data_dir'] = params['dirs']['data'] + '/' + params['mol']['Name']

    print '----> Checking for directory existence'

    if not posixpath.exists(params['dirs']['work']):
        print '    Creating: ' + params['dirs']['work']
        os.makedirs(params['dirs']['work'])
    else:
        print '    Directory Exists: ' + params['dirs']['work']

    if not posixpath.exists(params['dirs']['run_work_dir']):
        print '    Creating: ' + params['dirs']['run_work_dir']
        os.makedirs(params['dirs']['run_work_dir'])
    else:
        print '    Directory Exists: ' + params['dirs']['run_work_dir']

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
        params['dirs']['run_data_dir'] += '/psovbr'
        if not posixpath.exists(params['dirs']['run_data_dir']):
            print '    Creating: ' + params['dirs']['run_data_dir']
            os.makedirs(params['dirs']['run_data_dir'])
        else:
            print '    Directory Exists: ' + params['dirs']['run_data_dir']
