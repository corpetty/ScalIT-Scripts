__author__ = 'Corey Petty'
# !/usr/bin/env python

import posix
import posixpath
import pinFiles  # generate *.pin files and *.sh script for *.pin/*.pout
import shFiles  # make *.sh script for *.hin/*.in
import inFiles  # generate *.hin and *.in files
import indexing  # calculates number of angular basis functions for .in files


def mka3(option, cmd, mol, hin_flags, dirs, opts, jmax, ngi, ndvr, nvar):
    """
    Functions to create files for convergence testing for tri-atomic molecules
    :param option: which variable is selected for the convergence testing
    :param cmd: 
    :param mol: data related to the molecule: 
                 {'name','mass(3)','rmin(3)','rmax(3)',
                  'Nmax(3)','Nmin(3)','re(3)'}
    :param hin_flags: 
    :param dirs: directories for the work {'pes','pes_data','bin','dat','work'}
    :param opts: options for PIST calculations, current has:
                 {'ndvr','opt0~3','bjQMR','pistConv',
                  'nState','fh0','fhgm','fpt'}
    :param jmax: 
    :param ngi: 
    :param ndvr: 
    :param nvar: 
    :return:
    """

    # Set suffix to what is being converged
    if option < 0:
        mol["suffix"] = "p"
    elif option == 0:
        mol["suffix"] = "j"
    elif option == 1:
        mol["suffix"] = "A0"
    elif option == 2:
        mol["suffix"] = "r"
    elif option == 3:
        mol["suffix"] = "R"
    else:
        mol["suffix"] = "J"

    # Set working directories, check to see if they exist, create if not.
    dirs['run_work_dir'] = dirs['work'] + mol['Name'] + mol['suffix'] + '/'

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

    data_base = dirs['run_data_dir'] + mol['Name'] + mol['suffix']

    file_base = dirs['run_work_dir'] + mol['Name'] + mol['suffix']

    if option < 0:  # the initial step, do VBR
        # cmd['np'] = 1 TODO: check to see if this is necessary
        pinFiles.mkpin(mol, dirs)
        pinFiles.mkpsh(mol, dirs)

    elif option == 0:  # jmax convergence
        for x in nvar:
            jmax[0] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            ndvr[2] = indexing.get3size(mol['permutation'], mol['parity'], mol['jtotal'], jmax[0])
            inFiles.mkhin(mol, dirs, jmax, ngi, ndvr, hin_flags, fhin, x)
            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            opts['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0], 
                                                            'nBR': ndvr[1], 'nA0': ndvr[2]}
            opts['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            opts['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            opts['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(opts, fin)

        shFiles.mkmsh(cmd, mol, dirs, nvar)

    # TODO: make sure that jkNum is greater than ndvr(3) or else error returns
    elif option == 1:  # Angular basis size convergence
        for x in nvar:
            ndvr[2] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, ngi, ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            opts['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                            'nBR': ndvr[1], 'nA0': ndvr[2]}
            opts['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            opts['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            opts['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(opts, fin)

        shFiles.mkmsh(cmd, mol, dirs, nvar)

    elif option == 2:  # little r convergence, (j1=j2)
        for x in nvar:
            ndvr[0] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, ngi, ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            opts['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                            'nBR': ndvr[1], 'nA0': ndvr[2]}
            opts['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            opts['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            opts['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(opts, fin)

        shFiles.mkmsh(cmd, mol, dirs, nvar)

    elif option == 3:  # Big R convergence, (j1=j2)
        for x in nvar:
            ndvr[1] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, ngi, ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            opts['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                            'nBR': ndvr[1], 'nA0': ndvr[2]}
            opts['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            opts['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            opts['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(opts, fin)

        shFiles.mkmsh(cmd, mol, dirs, nvar)

    else:  # J Total convergence
        for x in nvar:
            mol['jtotal'] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, ngi, ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            opts['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                            'nBR': ndvr[1], 'nA0': ndvr[2]}
            opts['opt3'] = '0 0 0 0 1\n'
            opts['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            opts['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            opts['fpt'] = data_base + '/pt_%{jtot}d%{suf}s' % {'jtot': x, 'suf': '.dat'}
            inFiles.mkin(opts, fin)

        shFiles.mkmsh(cmd, mol, dirs, nvar)