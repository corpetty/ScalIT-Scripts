__author__ = 'Corey Petty'
# !/usr/bin/env python

import pinFiles  # generate *.pin files and *.sh script for *.pin/*.pout
import inFiles  # generate *.hin and *.in files
import indexing  # calculates number of angular basis functions for .in files
from util import setDirectories, shFiles  # sets directory environment, if doesn't exist, creates


def mka4(params):
    """
    Functions to create files for convergence testing for tri-atomic params['mol']ecules
    :param params: Contains all data to create files for ScalIT
    :type params: dict
    """

    # Set parameters what is being converged
    if params['run_opts']['conv_option'] < 0:
        params['mol']["suffix"] = "p"
        variable = ''
    elif params['run_opts']['conv_option'] == 0:
        params['mol']["suffix"] = "j1"
        variable = "j1_max"
    elif params['run_opts']['conv_option'] == 1:
        params['mol']["suffix"] = "j2"
        variable = "j2_max"
    elif params['run_opts']['conv_option'] == 2:
        params['mol']["suffix"] = "th"
        variable = 'theta'
    elif params['run_opts']['conv_option'] == 3:
        variable = 'num_r1_functions'
        params['mol']["suffix"] = "r1"
    elif params['run_opts']['conv_option'] == 4:
        variable = 'num_r2_functions'
        params['mol']["suffix"] = "r2"
    elif params['run_opts']['conv_option'] == 5:
        params['mol']["suffix"] = "R"
        variable = 'num_Br_functions'
    else:
        params['mol']["suffix"] = "J"
        variable = "j_total"

    # Set working directories, check to see if they exist, create if not.
    setDirectories.set_default_directories(params)

    data_base = params['dirs']['run_data_dir'] + params['mol']['Name'] + params['mol']['suffix']
    file_base = params['dirs']['run_work_dir'] + params['mol']['Name'] + params['mol']['suffix']

    print '----> Creating run files'
    if params['run_opts']['conv_option'] < 0:  # the initial step, do VBR
        pinFiles.mkpin(params)
        pinFiles.mkpsh(params)
    else:
        for x in params['run_opts']['nvar']:
            params['hin_opts'][variable] = x
            indexing.check_jknum(params)
            fhin = '%(fb)s_%(x)d%(suf)s' % {'fb': file_base, 'x': x, 'suf': '.hin'}
            inFiles.mkhin(params, fhin, x)
            fin = '%(fb)s_%(x)d%(suf)s' % {'fb': file_base, 'x': x, 'suf': '.in'}
            params['in_opts']['ndvr'] = '4 %(nr1)d %(nr2)d %(nBR)d %(nA0)d\n' % \
                                        {'nr1': params['hin_opts']['num_r1_functions'],
                                         'nr2': params['hin_opts']['num_r2_functions'],
                                         'nBR': params['hin_opts']['num_Br_functions'],
                                         'nA0': params['hin_opts']['theta']}
            params['in_opts']['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
            params['in_opts']['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
            params['in_opts']['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
            inFiles.mkin(params['in_opts'], fin)
        shFiles.mkmsh(params)
