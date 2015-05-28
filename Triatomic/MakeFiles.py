__author__ = 'Corey Petty'
# !/usr/bin/env python

import pinFiles  # generate *.pin files and *.sh script for *.pin/*.pout
import inFiles  # generate *.hin and *.in files
import indexing  # calculates number of angular basis functions for .in files
from Util import setDirectories, shFiles  # sets directory environment, if doesn't exist, creates


def mka3(params):
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
        params['mol']["suffix"] = "j"
        variable = "jmax"
    elif params['run_opts']['conv_option'] == 1:
        params['mol']["suffix"] = "th"
        variable = 'theta'
    elif params['run_opts']['conv_option'] == 2:
        params['mol']["suffix"] = "r"
        variable = 'num_lr_functions'
    elif params['run_opts']['conv_option'] == 3:
        params['mol']["suffix"] = "R"
        variable = 'num_Br_functions'
    else:
        params['mol']["suffix"] = "J"
        variable = "jtotal"

    # Set working directories, check to see if they exist, create if not.
    setDirectories.set_default_directories(params)

    data_base = params['dirs']['run_data_dir'] + '/' + params['mol']['Name'] + params['mol']['suffix']
    file_base = params['dirs']['run_work_dir'] + '/' + params['mol']['Name'] + params['mol']['suffix']

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
            params['in_opts']['num_lr_functions'] = str(params['hin_opts']['num_lr_functions'])
            params['in_opts']['num_Br_functions'] = str(params['hin_opts']['num_Br_functions'])
            params['in_opts']['theta'] = str(params['hin_opts']['theta'])
            params['in_file_names']['fH0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat'
            params['in_file_names']['fH0gm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat'
            params['in_file_names']['fPt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat'
            inFiles.mkin(params['in_opts'], params['in_file_names'], fin)
        shFiles.mkmsh(params)
