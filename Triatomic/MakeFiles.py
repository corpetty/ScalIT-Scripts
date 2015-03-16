__author__ = 'Corey Petty'
# !/usr/bin/env python

import pinFiles  # generate *.pin files and *.sh script for *.pin/*.pout
import shFiles  # make *.sh script for *.hin/*.in
import inFiles  # generate *.hin and *.in files
import indexing  # calculates number of angular basis functions for .in files
from Util import setDirectories  # sets directory environment, if doesn't exist, creates


def mka3(run_options, mol, hin_flags, dirs, in_options):
    """
    Functions to create files for convergence testing for tri-atomic molecules
    :param run_options: which variable is selected for the convergence testing
    :param mol: data related to the molecule: 
                 {'name','mass(3)','rmin(3)','rmax(3)',
                  'Nmax(3)','Nmin(3)','re(3)'}
    :param hin_flags: 
    :param dirs: directories for the work {'pes','pes_data','bin','dat','work'}
    :param in_options: options for PIST calculations, current has:
                 {'ndvr','opt0~3','bjQMR','pistConv',
                  'nState','fh0','fhgm','fpt'}
    :return:
    """
    jmax = run_options['jmax']
    ndvr = run_options['ndvr']

    # Set suffix to what is being converged
    if run_options['conv_option'] < 0:
        mol["suffix"] = "p"
    elif run_options['conv_option'] == 0:
        mol["suffix"] = "j"
    elif run_options['conv_option'] == 1:
        mol["suffix"] = "A0"
    elif run_options['conv_option'] == 2:
        mol["suffix"] = "r"
    elif run_options['conv_option'] == 3:
        mol["suffix"] = "R"
    else:
        mol["suffix"] = "J"

    # Set working directories, check to see if they exist, create if not.
    setDirectories.set_default_directories(dirs, mol)

    data_base = dirs['run_data_dir'] + mol['Name'] + mol['suffix']

    file_base = dirs['run_work_dir'] + mol['Name'] + mol['suffix']

    if run_options['conv_option'] < 0:  # the initial step, do VBR
        # cmd['np'] = 1 TODO: check to see if this is necessary
        pinFiles.mkpin(mol, dirs)
        pinFiles.mkpsh(mol, dirs)

    elif run_options['conv_option'] == 0:  # jmax convergence
        for x in run_options['nvar']:
            jmax[0] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            ndvr[2] = indexing.get3size(mol['permutation'], mol['parity'], mol['jtotal'], jmax[0])
            inFiles.mkhin(mol, dirs, jmax, run_options['ngi'], ndvr, hin_flags, fhin, x)
            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(mol, dirs, run_options)

    # TODO: make sure that jkNum is greater than ndvr(3) or else error returns
    elif run_options['conv_option'] == 1:  # Angular basis size convergence
        for x in run_options['nvar']:
            ndvr[2] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, run_options['ngi'], ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(mol, dirs, run_options)

    elif run_options['conv_option'] == 2:  # little r convergence, (j1=j2)
        for x in run_options['nvar']:
            ndvr[0] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, run_options['ngi'], ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(mol, dirs, run_options)

    elif run_options['conv_option'] == 3:  # Big R convergence, (j1=j2)
        for x in run_options['nvar']:
            ndvr[1] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, run_options['ngi'], ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(mol, dirs, run_options)

    else:  # J Total convergence
        for x in run_options['nvar']:
            mol['jtotal'] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(mol, dirs, jmax, run_options['ngi'], ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['opt3'] = '0 0 0 0 1\n'
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '/pt_%{jtot}d%{suf}s' % {'jtot': x, 'suf': '.dat'}
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(mol, dirs, run_options)