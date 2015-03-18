__author__ = 'Corey Petty'
# !/usr/bin/env python

import sys
import pinFiles  # generate *.pin files and *.sh script for *.pin/*.pout
import shFiles  # make *.sh script for *.hin/*.in
import inFiles  # generate *.hin and *.in files
import indexing  # calculates number of angular basis functions for .in files
import Converge
from Util import setDirectories  # sets directory environment, if doesn't exist, creates


def mka3(params):
    """
    Functions to create files for convergence testing for tri-atomic params['mol']ecules


    :param params: Contains all data to create files for ScalIT
    :type params: dict
    """

    if params['hin_opts']['restrict_num_angles'] == 'T':
        params['hin_opts']['theta'] = params['hin_opts']['num_angles']
    else:
        params['hin_opts']['theta'] = indexing.get3size(params)

    if (indexing.get3size(params['hin_opts']['permutation'],
                          params['hin_opts']['parity'],
                          params['hin_opts']['jtotal'],
                          params['hin_opts']['jmax']) < params['hin_opts']['num_angles']
            and params['hin_opts']['restrict_num_angles'] == 'T'):
        print 'Error:  Desired number of angles is greater than amount possible!'
        print '            Options:'
        print '                increase jmax'
        print '                decrease desired number of angles'
        print "                change 'restrict_num_angles' flag to 'F' (uses jkNum)"
        sys.exit(0)

    # Set suffix to what is being converged
    if params['run_opts']['conv_option'] < 0:
        params['mol']["suffix"] = "p"
    elif params['run_opts']['conv_option'] == 0:
        params['mol']["suffix"] = "j"
    elif params['run_opts']['conv_option'] == 1:
        params['mol']["suffix"] = "th"
    elif params['run_opts']['conv_option'] == 2:
        params['mol']["suffix"] = "r"
    elif params['run_opts']['conv_option'] == 3:
        params['mol']["suffix"] = "R"
    else:
        params['mol']["suffix"] = "J"

    # Set working directories, check to see if they exist, create if not.
    setDirectories.set_default_directories(params)

    data_base = params['dirs']['run_data_dir'] + params['mol']['Name'] + params['mol']['suffix']

    file_base = params['dirs']['run_work_dir'] + params['mol']['Name'] + params['mol']['suffix']

    print '----> Creating run files'
    if params['run_opts']['conv_option'] < 0:  # the initial step, do VBR
        pinFiles.mkpin(params)
        pinFiles.mkpsh(params)

    elif params['run_opts']['conv_option'] == 0:  # jmax convergence
        Converge.jmax(params)

    elif params['run_opts']['conv_option'] == 1:  # Angular basis size convergence
        Converge.theta(params)

    elif params['run_opts']['conv_option'] == 2:  # little r convergence
        for x in params['run_opts']['nvar']:
            ndvr[0] = x
            fhin = '%(fb)s_%(lr)d%(suf)s' % {'fb': file_base, 'lr': x, 'suf': '.hin'}
            inFiles.mkhin(params['mol'], params['dirs'], jmax, params['run_opts']['ngi'], ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(lr)d%(suf)s' % {'fb': file_base, 'lr': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(params['mol'], params['dirs'], params['run_opts'])

    elif params['run_opts']['conv_option'] == 3:  # Big R convergence
        for x in params['run_opts']['nvar']:
            ndvr[1] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(params['mol'], params['dirs'], jmax, params['run_opts']['ngi'], ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(params['mol'], params['dirs'], params['run_opts'])

    else:  # J Total convergence
        for x in params['run_opts']['nvar']:
            params['mol']['jtotal'] = x
            fhin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.hin'}
            inFiles.mkhin(params['mol'], params['dirs'], jmax, params['run_opts']['ngi'], ndvr, hin_flags, fhin, x)

            fin = '%(fb)s_%(j1)d%(suf)s' % {'fb': file_base, 'j1': x, 'suf': '.in'}
            in_options['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': ndvr[0],
                                                                  'nBR': ndvr[1], 'nA0': ndvr[2]}
            in_options['opt3'] = '0 0 0 0 1\n'
            in_options['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            in_options['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            in_options['fpt'] = data_base + '/pt_%{jtot}d%{suf}s' % {'jtot': x, 'suf': '.dat'}
            inFiles.mkin(in_options, fin)

        shFiles.mkmsh(params['mol'], params['dirs'], params['run_opts'])