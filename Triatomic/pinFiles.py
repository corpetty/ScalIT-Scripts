__author__ = 'Corey Petty'
# !/bin/env python

#
# make pin files for tetra-atomic molecules
#
import posix
import mkA3msh


def mkpsh(cmd, mol, dirs):
    """
    Create *.sh script files for PRESINC sequential module.
    :param cmd: 
    :param mol: 
    :param dirs: 
    :return:
    """

    mol_name = mol['Name']
    sfile = dirs['work'] + mol_name + '/' + mol_name + '.sh'

    work_base = '$WK_DIR/' + mol_name
    fpin_lr = work_base + 'lr.pin'
    fpout_lr = work_base + 'lr.pout'
    fpin_br = work_base + 'BR.pin'
    fpout_br = work_base + 'BR.pout'

    bin_base = '$BIN_DIR/' + mol_name + '/' + mol_name
    plr_cmd = bin_base + 'vlr'
    pbr_cmd = bin_base + 'vbr'

    fh = open(sfile, 'w')

    header = mkA3msh.get_sh_header(mol, dirs)
    fh.write(header)

    fh.write(plr_cmd + ' < ' + fpin_lr + ' > ' + fpout_lr + '\n')

    fh.write(pbr_cmd + ' < ' + fpin_br + ' > ' + fpout_br + '\n\n')
    fh.close()
    posix.system('chmod u+x ' + sfile)


def mkpin(cmd, mol, dirs):
    """ 
    Create the header of *.pin script files.
    :param cmd: NOT QUITE SURE WHY THIS IS HERE.
    :param mol:  run parameters of working molecule
    :param dirs: relevant directories of host
    :return: null
    """
    data_dir = dirs['data'] + mol['Name'] + '/' + mol['Name']
    pes_dir = dirs['pes'] + mol['Name'] + '/' + mol['Name']
    work_base = dirs['work'] + mol['Name'] + '/' + mol['Name']

    vlr = data_dir + 'vlr.dat'
    vbr = data_dir + 'vbr.dat'

    plr = pes_dir + '_vlr.dat'
    pbr = pes_dir + '_vbr.dat'

    dvr_type = mol['dvr_type']
    i = 0
    header = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
             % {'type': dvr_type, 'mass': mol['mass'][i], 'nmax': mol['Nmax'][i],
                'nmin': mol['Nmin'][i], 'useSP': mol['useSP']} \
             + '%(Rmin)f %(Rmax)f\n' % {'Rmin': mol['Rmin'][i], 'Rmax': mol['Rmax'][i]}

    fh = open(work_base + 'lr.pin', 'w')
    fh.write(header)
    fh.write(vlr + '\n')
    if mol['useSP'] == 'T':
        fh.write(plr + '\n')
    fh.close()

    i = 1
    header = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
             % {'type': dvr_type, 'mass': mol['mass'][i], 'nmax': mol['Nmax'][i],
                'nmin': mol['Nmin'][i], 'useSP': mol['useSP']} \
             + '%(Rmin)f %(Rmax)f\n' % {'Rmin': mol['Rmin'][i], 'Rmax': mol['Rmax'][i]}

    fh = open(work_base + 'BR.pin', 'w')
    fh.write(header)
    fh.write(vbr + '\n')
    if mol['useSP'] == 'T':
        fh.write(pbr + '\n')
    fh.close()


