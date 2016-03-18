__author__ = 'Corey Petty'


def check_rp_errors(params, variables) -> bool:
    for lrs in variables[1]:
        if lrs > params['pin_opts']['max_DVR_fns']:
            print('Current values:')
            print('   lr:       {}'.format(lrs))
            print('   max DVR:  {}'.format(params['pin_opts']['max_DVR_fns']))
            print('ERROR: The number of lr basis functions exceeds the maximum created from step 1.')
            print('       Please either rerun step two with larger max_DVR_functions or lower lr')
            return True
    for brs in variables[2]:
        if brs > params['pin_opts']['max_DVR_fns']:
            print('   br:       {}'.format(brs))
            print('   max DVR:  {}'.format(params['pin_opts']['max_DVR_fns']))
            print('ERROR: The number of br basis functions exceeds the maximum created from step 1.')
            print('       Please either rerun step two with larger max_DVR_functions or lower br')
            return True
    return False


def check_if_using_ceiling(angle_ceiling, jk_num):
    if angle_ceiling == 0:
        pass
    else:
        if jk_num > angle_ceiling:
            print('WARNING:  calculated number of angles exceeds ceiling value, using ceiling.')
            print('          num angles calculated:    {}'.format(jk_num))
            print('          ceiling value:            {}'.format(angle_ceiling))
