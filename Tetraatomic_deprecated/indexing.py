__author__ = 'Corey Petty'
import sys


def get4size(permutation, parity, j_total, j1_max, j2_max, j_max):
    """

    Calculates jkNum for tetra atomic molecules in ScalIT.
    :param permutation:
    :param parity:
    :param j_total:
    :param j1_max:
    :param j2_max:
    :param j_max:
    :return: jkNum
    """
    global jk_num
    jk_num = 0
    if permutation == "Agg":
        for j1 in range(0, j1_max + 1, 2):
            for j2 in range(0, j2_max + 1, 2):
                j0_min = abs(j1 - j2)
                j0_max = min(j1 + j2, j_max)
                for j in range(j0_min, j0_max + 1):
                    k0_max = min(j, j_total)
                    j_sum = j1 + j2 + j + j_total
                    if not parity:
                        j_sum += 1
                    if j_sum % 2 == 0:
                        k_min = 0
                    else:
                        k_min = 1
                    jk_num = jk_num + k0_max + 1 - k_min
    elif permutation == "Auu":
        for j1 in range(1, j1_max + 1, 2):
            for j2 in range(1, j2_max + 1, 2):
                j0_min = abs(j1 - j2)
                j0_max = min(j1 + j2, j_max)
                for j in range(j0_min, j0_max + 1):
                    k0_max = min(j, j_total)
                    j_sum = j1 + j2 + j + j_total
                    if not parity:
                        j_sum += 1
                    if j_sum % 2 == 0:
                        k_min = 0
                    else:
                        k_min = 1
                    jk_num = jk_num + k0_max + 1 - k_min
    elif permutation == "Agu":
        for j1 in range(0, j1_max + 1, 2):
            for j2 in range(1, j2_max + 1, 2):
                j0_min = abs(j1 - j2)
                j0_max = min(j1 + j2, j_max)
                for j in range(j0_min, j0_max + 1):
                    k0_max = min(j, j_total)
                    j_sum = j1 + j2 + j + j_total
                    if not parity:
                        j_sum += 1
                    if j_sum % 2 == 0:
                        k_min = 0
                    else:
                        k_min = 1
                    jk_num = jk_num + k0_max + 1 - k_min
    elif permutation == "Aug":
        for j1 in range(1, j1_max + 1, 2):
            for j2 in range(0, j2_max + 1, 2):
                j0_min = abs(j1 - j2)
                j0_max = min(j1 + j2, j_max)
                for j in range(j0_min, j0_max + 1):
                    k0_max = min(j, j_total)
                    j_sum = j1 + j2 + j + j_total
                    if not parity:
                        j_sum += 1
                    if j_sum % 2 == 0:
                        k_min = 0
                    else:
                        k_min = 1
                    jk_num = jk_num + k0_max + 1 - k_min
    else:
        print "You've chose an incorrect permutation:" \
              "    options include:" \
              "         Agg" \
              "         Auu" \
              "         Agu" \
              "         Aug"
    return jk_num


def check_jknum(params):
    if params['hin_opts']['restrict_num_angles'] == 'T':
        params['hin_opts']['theta'] = params['hin_opts']['num_angles']
    else:
        params['hin_opts']['theta'] = get4size(params['hin_opts']['permutation'],
                                               params['hin_opts']['parity'],
                                               params['hin_opts']['j_total'],
                                               params['hin_opts']['j1_max'],
                                               params['hin_opts']['j2_max'],
                                               params['hin_opts']['j_max'])

    if (get4size(params['hin_opts']['permutation'],
                 params['hin_opts']['parity'],
                 params['hin_opts']['j_total'],
                 params['hin_opts']['j1_max'],
                 params['hin_opts']['j2_max'],
                 params['hin_opts']['j_max']) < params['hin_opts']['num_angles']
            and params['hin_opts']['restrict_num_angles'] == 'T'):
        print 'Error:  Desired number of angles is greater than amount possible!'
        print '            Options:'
        print '                increase j1_max, j2_max, or j_max'
        print '                decrease desired number of angles'
        print "                change 'restrict_num_angles' flag to 'F' (uses jkNum)"
        sys.exit(0)
