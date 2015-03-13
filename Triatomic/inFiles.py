__author__ = 'Corey Petty'


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


def mkhin(mol, dirs, jmax, ngi, ndvr, flags, fname, var):
    """
    Generate the *.hin file for tri-atomics molecules for use in the
        2nd Step of the ScalIT suite.
    :param mol: parameters of the current molecule
    :param dirs: relevant directories
    :param jmax: 
    :param ngi:
    :param ndvr:
    :param flags:
    :param fname:
    :param var:
    :return:
    """
    psovbr_data_base = dirs['psodata'] + mol['Name']
    data_base = dirs['data'] + 'input/' + mol['Name']
    pes_data_base = dirs['pesData'] + mol['Name'] + '/' + mol['Name']
    mass = mol['mass']
    re = mol['re']

    h0 = data_base + mol['suffix'] + '_' + '%(var)d' % {'var': var} + 'h0.dat'
    h1 = data_base + mol['suffix'] + '_' + '%(var)d' % {'var': var} + 'hgm.dat'
    hre = data_base + mol['suffix'] + '_' + '%(var)d' % {'var': var} + 'hre.dat'

    # Setting string base for PSOVBR data file locations.
    vlr = psovbr_data_base + 'vlr.dat'
    vbr = psovbr_data_base + 'vbr.dat'

    plr = pes_data_base + '_vlr.dat'
    pbr = pes_data_base + '_vbr.dat'

    write_string = '%(jtol)d %(parity)s\n' % {'jtol': mol['jtotal'], 'parity': mol['parity']}

    write_string += '%(jmax)d %(ngi)d \n' % {('jmax'): jmax[0], ('ngi'): ngi[0]}

    write_string += '%(FcFlag)d %(CbFlag)d %(AbsFlag)d %(useSP)s %(Ecutoff)f\n' \
                    % {'FcFlag': flags['FcFlag'], 'CbFlag': flags['CbFlag'], 'AbsFlag': flags['AbsFlag'],
                       'useSP': mol['useSP'], 'Ecutoff': flags['Ecutoff']}

    write_string += h0 + '\n' + h1 + '\n'

    write_string += '%(mass1)f %(re1)f %(ndvr1)d\n' \
                    % {'mass1': mass[0], 're1': re[0], 'ndvr1': ndvr[0]}
    write_string += vlr + '\n'

    write_string += '%(mass1)f %(re1)f %(ndvr1)d\n' \
                    % {'mass1': mass[1], 're1': re[1], 'ndvr1': ndvr[1]}
    write_string += vbr + '\n'

    write_string += '%(ndvr)d %(reFlag)d\n' \
                    % {'ndvr': ndvr[2], 'reFlag': flags['ReFlag']}
    write_string += hre + '\n'

    if mol['useSP'] == 'T':
        write_string += plr + '\n' + pbr + '\n'

    fhin = open(fname, 'w')
    fhin.write(write_string)
    fhin.close()

