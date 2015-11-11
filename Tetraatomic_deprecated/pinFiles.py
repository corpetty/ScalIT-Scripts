__author__ = 'Corey Petty'
# !/bin/env python

import posix

from util import shFiles


def mkpsh(params):
    """
    Create *.sh script files for PRESINC sequential module.
    :param params['mol']:
    :param params['dirs']:
    :return:
    """

    script_file = params['dirs']['run_work_dir'] + params['mol']['Name'] + '.sh'
    work_base = "$WK_DIR/" + params['mol']['Name']

    fpin_r1 = work_base + 'r1.pin'
    fpout_r1 = work_base + 'r1.pout'
    fpin_r2 = work_base + 'r2.pin'
    fpout_r2 = work_base + 'r2.pout'
    fpin_br = work_base + 'BR.pin'
    fpout_br = work_base + 'BR.pout'

    bin_base = "$BIN_DIR/" + params['mol']['Name'] + '/' + params['mol']['Name']
    pr1_cmd = bin_base + 'vlr'
    pr2_cmd = bin_base + 'vlr'
    pbr_cmd = bin_base + 'vbr'

    fh = open(script_file, 'w')

    header = shFiles.get_sh_header(params)
    fh.write(header)

    fh.write(pr1_cmd + ' < ' + fpin_r1 + ' > ' + fpout_r1 + '\n')

    fh.write(pr2_cmd + ' < ' + fpin_r2 + ' > ' + fpout_r2 + '\n')

    fh.write(pbr_cmd + ' < ' + fpin_br + ' > ' + fpout_br + '\n\n')
    fh.close()
    print '    File Generated: ' + script_file
    posix.system('chmod u+x ' + script_file)


def mkpin(params):
    """
    Create the header of *.pin script files.
    :param params['mol']:  run parameters of working params['mol']ecule
    :param params['dirs']: relevant directories of host
    :return: null
    """

    pes_data_base = params['dirs']['pes_data'] + params['mol']['Name'] + '/' + params['mol']['Name']
    work_base = params['dirs']['run_work_dir'] + params['mol']['Name']
    data_base = params['dirs']['run_data_dir'] + params['mol']['Name']

    # Setting up string base for output files of *.pin
    vr1 = data_base + 'vr1.dat'
    vr2 = data_base + 'vr2.dat'
    vbr = data_base + 'vbr.dat'

    # Setting up string base for PES eff potential input files
    pr1 = pes_data_base + '_vr1.dat'
    pr2 = pes_data_base + '_vr2.dat'
    pbr = pes_data_base + '_vbr.dat'

    i = 0  # reference to r1
    header = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
             % {'type': params['pin_opts']['dvr_type'],
                'mass': params['mol']['mass'][i],
                'nmax': params['pin_opts']['num_sinc_fns'][i],
                'nmin': params['pin_opts']['max_DVR_fns'][i],
                'useSP': params['pin_opts']['useSP']} \
             + '%(Rmin)f %(Rmax)f\n' % {'Rmin': params['mol']['Rmin'][i],
                                        'Rmax': params['mol']['Rmax'][i]}
    fh = open(work_base + 'r1.pin', 'w')
    fh.write(header)
    fh.write(vr1 + '\n')
    if params['pin_opts']['useSP'] == 'T':
        fh.write(pr1 + '\n')
    fh.close()
    print '    File Generated: ' + work_base + 'r1.pin'

    i = 1  # reference to r2
    header = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
             % {'type': params['pin_opts']['dvr_type'],
                'mass': params['mol']['mass'][i],
                'nmax': params['pin_opts']['num_sinc_fns'][i],
                'nmin': params['pin_opts']['max_DVR_fns'][i],
                'useSP': params['pin_opts']['useSP']} \
             + '%(Rmin)f %(Rmax)f\n' % {'Rmin': params['mol']['Rmin'][i],
                                        'Rmax': params['mol']['Rmax'][i]}
    fh = open(work_base + 'r2.pin', 'w')
    fh.write(header)
    fh.write(vr2 + '\n')
    if params['pin_opts']['useSP'] == 'T':
        fh.write(pr2 + '\n')
    fh.close()
    print '    File Generated: ' + work_base + 'r2.pin'

    i = 2  # reference to BR
    header = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
             % {'type': params['pin_opts']['dvr_type'],
                'mass': params['mol']['mass'][i],
                'nmax': params['pin_opts']['num_sinc_fns'][i],
                'nmin': params['pin_opts']['max_DVR_fns'][i],
                'useSP': params['pin_opts']['useSP']} \
             + '%(Rmin)f %(Rmax)f\n' % {'Rmin': params['mol']['Rmin'][i],
                                        'Rmax': params['mol']['Rmax'][i]}
    fh = open(work_base + 'BR.pin', 'w')
    fh.write(header)
    fh.write(vbr + '\n')
    if params['pin_opts']['useSP'] == 'T':
        fh.write(pbr + '\n')
    fh.close()
    print '    File Generated: ' + work_base + 'BR.pin'


