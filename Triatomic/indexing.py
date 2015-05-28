__author__ = 'Corey Petty'
import sys


def get3size(permutation, parity, j_tot, j_max):
    """
    This function calculates the size of the combined angular basis
    for triatomic molecules as defined by the
    ScalIT/index/index_AB2(e/o).f90 files.
    :param permutation: 'e' or 'o'
    :param parity: 'T' or 'F'
    :param j_tot: Total angular momentum quantum number, J
    :type j_tot: int
    :param j_max: angular momentum associated with little r
    :type j_max: int
    :return: int
    """
    global size
    if permutation == 'e':
        if parity == 'T':
            jp = 0
        elif parity == 'F':
            jp = 1
        else:
            print 'Incorrect parity option, choose (T,F)'
            return 0
        jt = j_tot + jp

        if jt / 2 * 2 == jt:
            k_min = 0
        else:
            k_min = 1

        size = 0
        for j in range(0, j_max + 1):
            k_max = min(j_tot, j)
            for k in range(k_min, k_max + 1):
                jk = j + jp
                if jk / 2 * 2 == jk:
                    size += 1
    elif permutation == 'o':  # even permutation
        if parity == 'T':  # even parity
            jp = 0
        elif parity == 'F':  # odd parity
            jp = 1
        else:
            print 'Incorrect parity option, choose (T,F)'
            return 0
        jt = j_tot + jp  # total parity = (-1)^(p+JTol)

        if jt == jt / 2 * 2:  # even total parity
            k_min = 0
        else:
            k_min = 1
        size = 0
        for j in range(0, j_max + 1):
            k_max = min(j_tot, j)
            for k in range(k_min, k_max + 1):
                jk = j + jp
                if jk / 2 * 2 != jk:
                    size += 1
    return size


def check_jknum(params):
    if params['hin_opts']['restrict_num_angles'] == 'T':
        params['hin_opts']['theta'] = params['hin_opts']['num_angles']
    else:
        params['hin_opts']['theta'] = get3size(params['hin_opts']['permutation'],
                                               params['hin_opts']['parity'],
                                               params['hin_opts']['jtotal'],
                                               params['hin_opts']['jmax'])
    if (get3size(params['hin_opts']['permutation'],
                 params['hin_opts']['parity'],
                 params['hin_opts']['j_total'],
                 params['hin_opts']['jmax']) < params['hin_opts']['num_angles']
            and params['hin_opts']['restrict_num_angles'] == 'T'):
        print 'Error:  Desired number of angles is greater than amount possible!'
        print '            Options:'
        print '                increase jmax'
        print '                decrease desired number of angles'
        print "                change 'restrict_num_angles' flag to 'F' (uses jkNum)"
        sys.exit(0)
