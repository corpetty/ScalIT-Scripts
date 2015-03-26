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
    vr1 = psovbr_data_base + 'vr1.dat'
    vr2 = psovbr_data_base + 'vr2.dat'
    vbr = psovbr_data_base + 'vbr.dat'

    pr1 = pes_data_base + '_vr1.dat'
    pr2 = pes_data_base + '_vr2.dat'
    pbr = pes_data_base + '_vbr.dat'

    write_string = '%(jtol)d %(parity)s\n' % {'jtol': params['hin_opts']['j_total'],
                                              'parity': params['hin_opts']['parity']}

    write_string += '%(j1max)d %(j2max)d %(jmax)d %(ngi)d %(ngi)d %(ngi)d \n' % \
                    {'j1max': params['hin_opts']['j1_max'],
                     'j2max': params['hin_opts']['j2_max'],
                     'jmax': params['hin_opts']['j_max'],
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
                       'ndvr1': params['hin_opts']['num_r1_functions']}
    write_string += vr1 + '\n'

    write_string += '%(mass2)f %(re2)f %(ndvr2)d\n' \
                    % {'mass2': params['mol']['mass'][1],
                       're2': params['mol']['re'][1],
                       'ndvr2': params['hin_opts']['num_r2_functions']}
    write_string += vr2 + '\n'

    write_string += '%(mass3)f %(re3)f %(ndvr3)d\n' \
                    % {'mass3': params['mol']['mass'][2],
                       're3': params['mol']['re'][2],
                       'ndvr3': params['hin_opts']['num_Br_functions']}
    write_string += vbr + '\n'

    write_string += '%(ndvr)d %(reFlag)d\n' \
                    % {'ndvr': params['hin_opts']['theta'],
                       'reFlag': params['hin_opts']['ReFlag']}
    write_string += hre + '\n'

    if params['pin_opts']['useSP'] == 'T':
        write_string += pr1 + '\n' + pr2 + '\n' + pbr + '\n'

    fhin = open(fname, 'w')
    fhin.write(write_string)
    fhin.close()
    print '    File Generated: ' + fname

