__author__ = 'coreypetty'
#
# Generate the *.in file for tri-atomic molecules
#

def mkin(opts,fname):

    fh1=open(fname,'w')
    fh1.write( opts['ndvr'] )
    fh1.write( opts['opt0'] )
    fh1.write( opts['opt1'] )
    fh1.write( opts['opt2'] )
    fh1.write( opts['bjQMR'])
    fh1.write( opts['pistConv'])
    fh1.write( opts['nState'])
    fh1.write( opts['opt3'] )
    fh1.write( opts['fh0']  )
    fh1.write( opts['fhgm'] )
    fh1.write( opts['fpt']  )
    fh1.close()

#
# make hin file for tri-atomic molecules
#
def mkhin(mol, dirs, jmax, ngi, ndvr, flags, fname, var):
    datBase = dirs['data']+'input/'+mol['Name']
    pesBase = dirs['pes']+mol['Name']+'/'+mol['Name']
    pesDataBase = dirs['pesData']+mol['Name']+'/'+mol['Name']
    mass = mol['mass'];   re=mol['re']

    h0  = datBase+mol['suffix']+'_'+'%(var)d'%{'var':var}+'h0.dat'
    h1  = datBase+mol['suffix']+'_'+'%(var)d'%{'var':var}+'hgm.dat'
    hre = datBase+mol['suffix']+'_'+'%(var)d'%{'var':var}+'hre.dat'

    vlr  = datBase+'vlr.dat';
    vBR  = datBase+'vBR.dat'

    plr  = pesDataBase+'_vlr.dat';
    pBR  = pesDataBase+'_vBR.dat'

    str='%(jtol)d %(parity)s\n' %{'jtol':mol['jtotal'],'parity':mol['parity']}

    str += '%(jmax)d %(ngi)d \n' %{('jmax'):jmax[0], ('ngi'):ngi[0]}

    str += '%(FcFlag)d %(CbFlag)d %(AbsFlag)d %(useSP)s %(Ecutoff)f\n' \
           %{'FcFlag':flags['FcFlag'],'CbFlag':flags['CbFlag'],'AbsFlag':flags['AbsFlag'], \
             'useSP':mol['useSP'],'Ecutoff':flags['Ecutoff']}
    str += h0 + '\n' + h1 + '\n'

    str += '%(mass1)f %(re1)f %(ndvr1)d\n' \
           %{'mass1':mass[0],'re1':re[0],'ndvr1':ndvr[0]}
    str += vlr + '\n'

    str += '%(mass1)f %(re1)f %(ndvr1)d\n' \
           %{'mass1':mass[1],'re1':re[1],'ndvr1':ndvr[1]}
    str += vBR + '\n'

    str += '%(ndvr)d %(reFlag)d\n' \
           %{'ndvr':ndvr[2],'reFlag':flags['ReFlag']}
    str += hre + '\n'

    if (mol['useSP']=='T'):
       str += plr+'\n'+pBR+'\n'

    fhin=open(fname,'w')
    fhin.write(str)
    fhin.close()

