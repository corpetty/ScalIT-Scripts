__author__ = 'Corey Petty'

import posix
import posixpath


def set_default_directories(dirs, mol):
    """
    Routine to set up default directories from user inputed directories
    :param dirs: Directory dictionary started by user in input parameter file
    :param mol: Molecular parameters, need 'Name' and 'suffix'
    :return:
    """
    dirs['bin'] = dirs['scalit'] + 'bin/'
    dirs['pes'] = dirs['scalit'] + 'src/systems/'
    dirs['work'] = dirs['scalit'] + 'work/test/'
    dirs['pes_data'] = dirs['scalit'] + 'data/'
    dirs['run_work_dir'] = dirs['work'] + mol['Name'] + mol['suffix'] + '/'
    dirs['run_data_dir'] = dirs['data'] + mol['Name'] + '/'

    print '----> Checking for directory existence'

    if not posixpath.exists(dirs['work']):
        print '     Creating: ' + dirs['work']
        posix.mkdir(dirs['work'])
    else:
        print '     Directory Exists: ' + dirs['work']

    if not posixpath.exists(dirs['run_work_dir']):
        print '     Creating: ' + dirs['run_work_dir']
        posix.mkdir(dirs['run_work_dir'])
    else:
        print '     Directory Exists: ' + dirs['run_work_dir']

    if not posixpath.exists(dirs['data']):
        print '     Creating: ' + dirs['data']
        posix.mkdir(dirs['data'])
    else:
        print '     Directory Exists: ' + dirs['data']

    if not posixpath.exists(dirs['run_data_dir']):
        print '     Creating: ' + dirs['run_data_dir']
        posix.mkdir(dirs['run_data_dir'])
    else:
        print '     Directory Exists: ' + dirs['run_data_dir']

    if mol['suffix'] == 'p':
        dirs['run_data_dir'] += 'psovbr/'
        if not posixpath.exists(dirs['run_data_dir']):
            print '     Creating: ' + dirs['run_data_dir']
            posix.mkdir(dirs['run_data_dir'])
        else:
            print '     Directory Exists: ' + dirs['run_data_dir']