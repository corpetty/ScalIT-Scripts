__author__ = 'Corey Petty'
# !/bin/env python

import posix
import shFiles


def mkpsh(mol, dirs):
    """
    Create *.sh script files for PRESINC sequential module.
    :param mol: 
    :param dirs: 
    :return:
    """
    
    script_file = dirs['run_work_dir'] + mol['Name'] + '.sh'

    work_base = dirs['run_work_dir'] + '/' + mol['Name']
    fpin_lr = work_base + 'lr.pin'
    fpout_lr = work_base + 'lr.pout'
    fpin_br = work_base + 'BR.pin'
    fpout_br = work_base + 'BR.pout'

    bin_base = dirs['bin'] + mol['Name'] + '/' + mol['Name']
    plr_cmd = bin_base + 'vlr'
    pbr_cmd = bin_base + 'vbr'

    fh = open(script_file, 'w')

    header = shFiles.get_sh_header(mol, dirs)
    fh.write(header)

    fh.write(plr_cmd + ' < ' + fpin_lr + ' > ' + fpout_lr + '\n')

    fh.write(pbr_cmd + ' < ' + fpin_br + ' > ' + fpout_br + '\n\n')
    fh.close()
    print '    File Generated: ' + script_file
    posix.system('chmod u+x ' + script_file)


def mkpin(mol, dirs):
    """ 
    Create the header of *.pin script files.
    :param mol:  run parameters of working molecule
    :param dirs: relevant directories of host
    :return: null
    """
    
    pes_data_base = dirs['pes_data'] + mol['Name'] + '/' + mol['Name']
    work_base = dirs['run_work_dir'] + mol['Name']
    data_base = dirs['run_data_dir'] + mol['Name']

    # Setting up string base for output files of *.pin
    vlr = data_base + 'vlr.dat'
    vbr = data_base + 'vbr.dat'

    # Setting up string base for PES eff potential input files
    plr = pes_data_base + '_vlr.dat'
    pbr = pes_data_base + '_vbr.dat'

    i = 0  # reference to lr
    header = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
             % {'type': mol['dvr_type'], 'mass': mol['mass'][i], 'nmax': mol['Nmax'][i],
                'nmin': mol['Nmin'][i], 'useSP': mol['useSP']} \
             + '%(Rmin)f %(Rmax)f\n' % {'Rmin': mol['Rmin'][i], 'Rmax': mol['Rmax'][i]}

    fh = open(work_base + 'lr.pin', 'w')
    fh.write(header)
    fh.write(vlr + '\n')
    if mol['useSP'] == 'T':
        fh.write(plr + '\n')
    fh.close()
    print '    File Generated: ' + work_base + 'lr.pin'

    i = 1  # reference to BR
    header = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
             % {'type': mol['dvr_type'], 'mass': mol['mass'][i], 'nmax': mol['Nmax'][i],
                'nmin': mol['Nmin'][i], 'useSP': mol['useSP']} \
             + '%(Rmin)f %(Rmax)f\n' % {'Rmin': mol['Rmin'][i], 'Rmax': mol['Rmax'][i]}

    fh = open(work_base + 'BR.pin', 'w')
    fh.write(header)
    fh.write(vbr + '\n')
    if mol['useSP'] == 'T':
        fh.write(pbr + '\n')
    fh.close()
    print '    File Generated: ' + work_base + 'BR.pin'


