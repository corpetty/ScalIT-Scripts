__author__ = 'Corey Petty'

import posixpath


def mkin(opts, fname):
    """
    Generate the *.in file for tri-atomic molecules for use in the
        3rd Step of the ScalIT suite
    
    :param opts: options, as defined
    :param fname: filename to be created
    :return:
    """
    fh1 = open(fname, 'w')
    fh1.write(opts['ndvr'])
    fh1.write(opts['opt0'])
    fh1.write(opts['opt1'])
    fh1.write(opts['opt2'])
    fh1.write(opts['bjQMR'])
    fh1.write(opts['pistConv'])
    fh1.write(opts['nState'])
    fh1.write(opts['opt3'])
    fh1.write(opts['fh0'])
    fh1.write(opts['fhgm'])
    fh1.write(opts['fpt'])
    fh1.close()
    print '    File Generated: ' + fname


def mkhin(params, fname, var):
    """
    Generate the *.hin file for tri-atomics params['mol']ecules for use in the
        2nd Step of the ScalIT suite.
    :param params: Dictionary of all run parameters
    :param fname: filename to be saved
    :param var: variable value of convergence parameter
    :type var: int
    :return:
    """
    if params['mol']['suffix'] != 'p':
        if not posixpath.exists(params['dirs']['data'] + params['mol']['Name'] + '/psovbr/'):
            print "     PRESINC data files aren't found, please run option = -1"

    psovbr_data_base = params['dirs']['data'] + params['mol']['Name'] + '/psovbr/' + params['mol']['Name']
    data_base = params['dirs']['data'] + params['mol']['Name'] + '/' + params['mol']['Name']
    pes_data_base = params['dirs']['pes_data'] + params['mol']['Name'] + '/' + params['mol']['Name']

    h0 = data_base + params['mol']['suffix'] + '_' + '%(var)d' % {'var': var} + 'h0.dat'
    h1 = data_base + params['mol']['suffix'] + '_' + '%(var)d' % {'var': var} + 'hgm.dat'
    hre = data_base + params['mol']['suffix'] + '_' + '%(var)d' % {'var': var} + 'hre.dat'

    # Setting string base for PSOVBR data file locations.
    vlr = psovbr_data_base + 'vlr.dat'
    vbr = psovbr_data_base + 'vbr.dat'

    plr = pes_data_base + '_vlr.dat'
    pbr = pes_data_base + '_vbr.dat'

    write_string = '%(jtol)d %(parity)s\n' % {'jtol': params['hin_opts']['jtotal'],
                                              'parity': params['hin_opts']['parity']}

    write_string += '%(jmax)d %(ngi)d \n' % {'jmax': params['hin_opts']['jmax'],
                                             'ngi': params['hin_opts']['ngi']}

    write_string += '%(FcFlag)d %(CbFlag)d %(AbsFlag)d %(useSP)s %(Ecutoff)f\n' \
                    % {'FcFlag': params['hin_opts']['FcFlag'],
                       'CbFlag': params['hin_opts']['CbFlag'],
                       'AbsFlag': params['hin_opts']['AbsFlag'],
                       'useSP': params['pin_opts']['useSP'],
                       'Ecutoff': params['hin_opts']['Ecutoff']}

    write_string += h0 + '\n' + h1 + '\n'

    write_string += '%(mass1)f %(re1)f %(ndvr1)d\n' \
                    % {'mass1': params['mol']['mass'][0],
                       're1': params['mol']['re'][0],
                       'ndvr1': params['hin_opts']['num_lr_functions']}
    write_string += vlr + '\n'

    write_string += '%(mass1)f %(re1)f %(ndvr1)d\n' \
                    % {'mass1': params['mol']['mass'][1],
                       're1': params['mol']['re'][1],
                       'ndvr1': params['hin_opts']['num_Br_functions']}
    write_string += vbr + '\n'

    write_string += '%(ndvr)d %(reFlag)d\n' \
                    % {'ndvr': params['hin_opts']['theta'],
                       'reFlag': params['hin_opts']['ReFlag']}
    write_string += hre + '\n'

    if params['pin_opts']['useSP'] == 'T':
        write_string += plr + '\n' + pbr + '\n'

    fhin = open(fname, 'w')
    fhin.write(write_string)
    fhin.close()
    print '    File Generated: ' + fname

