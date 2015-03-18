__author__ = 'Corey Petty'
import shFiles
import inFiles
import indexing


def jmax(params):
    """
    Routine to create files for converging jmax for triatomic molecules in ScalIT
    :param params: Complete set of parameters for run
    :type params: dict
    :return: null
    """
    file_base = params['dirs']['run_work_dir'] + params['mol']['Name'] + params['mol']['suffix']
    data_base = params['dirs']['run_data_dir'] + params['mol']['Name'] + params['mol']['suffix']
    for x in params['run_opts']['nvar']:
        params['hin_opts']['jmax'] = x
        fhin = '%(fb)s_%(x)d%(suf)s' % {'fb': file_base, 'x': x, 'suf': '.hin'}
        params['hin_opts']['theta'] = indexing.get3size(params['hin_opts']['permutation'],
                                                        params['hin_opts']['parity'],
                                                        params['hin_opts']['jtotal'],
                                                        x)
        inFiles.mkhin(params, fhin, x)
        fin = '%(fb)s_%(x)d%(suf)s' % {'fb': file_base, 'x': x, 'suf': '.in'}
        params['in_opts']['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': params['hin_opts']['num_lr_functions'],
                                                                     'nBR': params['hin_opts']['num_Br_functions'],
                                                                     'nA0': params['hin_opts']['theta']}
        params['in_opts']['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
        params['in_opts']['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
        params['in_opts']['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
        inFiles.mkin(params['in_opts'], fin)
    shFiles.mkmsh(params)


def theta(params):
    """
    Routine to create files for converging the total angular basis
    :param params:
    :return: null
    """
    file_base = params['dirs']['run_work_dir'] + params['mol']['Name'] + params['mol']['suffix']
    data_base = params['dirs']['run_data_dir'] + params['mol']['Name'] + params['mol']['suffix']
    for x in params['run_opts']['nvar']:
        params['hin_opts']['theta'] = x
        fhin = '%(fb)s_%(x)d%(suf)s' % {'fb': file_base, 'x': x, 'suf': '.hin'}
        inFiles.mkhin(params, fhin, x)
        fin = '%(fb)s_%(x)d%(suf)s' % {'fb': file_base, 'x': x, 'suf': '.in'}
        params['in_opts']['ndvr'] = '3 %(nlr)d %(nBR)d %(nA0)d\n' % {'nlr': params['hin_opts']['num_lr_functions'],
                                                                     'nBR': params['hin_opts']['num_Br_functions'],
                                                                     'nA0': params['hin_opts']['theta']}
        params['in_opts']['fh0'] = data_base + '_%(x)d' % {'x': x} + 'h0.dat\n'
        params['in_opts']['fhgm'] = data_base + '_%(x)d' % {'x': x} + 'hgm.dat\n'
        params['in_opts']['fpt'] = data_base + '_%(x)d' % {'x': x} + 'wf.dat\n'
        inFiles.mkin(params['in_opts'], fin)
    shFiles.mkmsh(params)