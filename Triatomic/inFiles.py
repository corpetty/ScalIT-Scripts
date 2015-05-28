__author__ = 'Corey Petty'

import posixpath


def mkin(opts, in_file_names, fname):
    """

    :param opts:
    :param fname:
    :return:
    """

    infile = open(fname, 'w')
    infile.write(opts['sF'] + ' '
                 + opts['num_lr_functions'] + ' '
                 + opts['num_Br_functions'] + ' '
                 + opts['theta']
                 + '\n')
    infile.write(opts['sDep'][0] + ' '
                 + opts['sDep'][1] + ' '
                 + opts['sDep'][2]
                 + '\n')
    infile.write(opts['sJOB'] + ' '
                 + opts['sOSB']
                 + '\n')
    infile.write(opts['sCX'] + ' '
                 + opts['sNDVR'] + ' '
                 + opts['sST'] + ' '
                 + opts['sAP']
                 + '\n')
    infile.write(opts['bj_NumberIters'] + ' '
                 + opts['bj_Tolerance'] + ' '
                 + opts['qmr_NumberIters'] + ' '
                 + opts['qmr_Tolerance']
                 + '\n')
    infile.write(opts['pist_E0'] + ' ' + opts['pist_LancToler'] + ' '
                 + opts['pist_nStart'] + ' '
                 + opts['pist_nStep'] + ' '
                 + opts['pist_nMax'] + ' '
                 + opts['pist_nGap']
                 + '\n')
    infile.write(opts['osb_mE0'] + ' '
                 + opts['osb_mDE'] + ' '
                 + opts['osb_mBeta'] + ' '
                 + opts['osb_nCnt']
                 + '\n')
    infile.write(opts['sHOSB'] + ' '
                 + opts['sVOSB'] + ' '
                 + opts['sHW'] + ' '
                 + opts['sVX'] + ' '
                 + opts['sPT']
                 + '\n')
    infile.write(in_file_names['fH0']
                 + '\n')
    infile.write(in_file_names['fH0gm']
                 + '\n')
    if opts['sDep'][0] == 'T':
        infile.write(in_file_names['fDep'][0]
                     + '\n')
    if opts['sDep'][1] == 'T':
        infile.write(in_file_names['fDep'][1]
                     + '\n')
    if opts['sDep'][2] == 'T':
        infile.write(in_file_names['fDep'][2]
                     + '\n')
    if opts['sHOSB'] != '0':
        infile.write(in_file_names['fHOSB']
                     + '\n')
    if opts['sVOSB'] != '0':
        infile.write(in_file_names['fVOSB']
                     + '\n')
    if opts['sHW'] != '0':
        infile.write(in_file_names['fHW']
                     + '\n')
    if opts['sVX'] != '0':
        infile.write(in_file_names['fVX']
                     + '\n')
    if opts['sPT'] != '0':
        infile.write(in_file_names['fPT']
                     + '\n')

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
        if not posixpath.exists(params['dirs']['data'] + '/' + params['mol']['Name'] + '/psovbr/'):
            print "     PRESINC data files aren't found, please run option = -1"

    psovbr_data_base = params['dirs']['data'] + '/' + params['mol']['Name'] + '/psovbr/' + 'presinc_'
    data_base = params['dirs']['data'] + '/' + params['mol']['Name'] + '/' + params['mol']['Name']
    pes_data_base = params['dirs']['pes_data'] + '/' + params['mol']['Name'] + '/' + params['mol']['Name']

    h0 = data_base + params['mol']['suffix'] + '_' + '%(var)d' % {'var': var} + 'h0.dat'
    h1 = data_base + params['mol']['suffix'] + '_' + '%(var)d' % {'var': var} + 'hgm.dat'
    hre = data_base + params['mol']['suffix'] + '_' + '%(var)d' % {'var': var} + 'hre.dat'

    # Setting string base for PSOVBR data file locations.
    vlr = psovbr_data_base + 'lr.dat'
    vbr = psovbr_data_base + 'br.dat'

    plr = pes_data_base + '_vlr.dat'
    pbr = pes_data_base + '_vbr.dat'

    write_string = '%(jtol)d %(parity)s ' % {'jtol': params['hin_opts']['j_total'],
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
