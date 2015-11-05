__author__ = 'Corey Petty'


def step_one(paths, files, mol, pin_options):
    """

    :param paths:
    :param files:
    :param mol:
    :param pin_options:
    :return:
    """
    #  Little r
    #    Create file substance, line by line
    line_one = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
               % {'type': pin_options.dvr_type,
                  'mass': mol.lr.mass,
                  'nmax': mol.lr.num_sinc_fns,
                  'nmin': mol.lr.num_vbr_fns,
                  'useSP': pin_options.use_spline
                  }
    line_two = '%(Rmin)f %(Rmax)f\n' \
               % {'Rmin': mol.lr.length[0],
                  'Rmax': mol.lr.length[1]
                  }

    line_three = '%(outfile)s' \
                 % {'outfile': paths.run_psovbr_data + '/' + files.psovbr_lr}

    #    Write the files
    fh = open(paths.run_psovbr + '/' + files.presinc_lr + files.input, 'w')
    fh.write(line_one + line_two + line_three)
    if pin_options.use_spline == "T":
        fh.write('\n' + paths.pes_data + '/' + files.v_eff_lr)
    fh.close()
    print '    File Generated: ' + paths.run_psovbr + '/' + files.presinc_lr + files.input

    #  Big R
    #    Create file substance, line by line
    line_one = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
               % {'type': pin_options.dvr_type,
                  'mass': mol.br.mass,
                  'nmax': mol.br.num_sinc_fns,
                  'nmin': mol.br.num_vbr_fns,
                  'useSP': pin_options.use_spline
                  }
    line_two = '%(Rmin)f %(Rmax)f\n' \
               % {'Rmin': mol.br.length[0],
                  'Rmax': mol.br.length[1]
                  }

    line_three = '%(outfile)s' \
                 % {'outfile': paths.run_psovbr_data + '/' + files.psovbr_br}

    #    Write the files
    fh = open(paths.run_psovbr + '/' + files.presinc_br + files.input, 'w')
    fh.write(line_one + line_two + line_three)
    if pin_options.use_spline == "T":
        fh.write('\n' + paths.pes_data + '/' + files.v_eff_br)
    fh.close()
    print '    File Generated: ' + paths.run_psovbr + '/' + files.presinc_br + files.input


def step_two(paths, files, mol, options):
    """
    Creates the Step Two (Hamiltonian Constructrion) input files.  Requires
    the following class instances.
    :param paths:
    :param files:
    :param mol:
    :param options:
    :return:
    """

    hin_file = [
        '%(jtol)d %(parity)s '
        % {'jtol': mol.j_total,
           'parity': 'F' if mol.parity == 'odd' else 'T'
           },
        '%(jmax)d %(ngi)d \n'
        % {'jmax': mol.j_max,
           'ngi': options.hin_options.ngi
           },
        '%(FcFlag)d %(CbFlag)d %(AbsFlag)d %(useSP)s %(Ecutoff)f\n'
        % {'FcFlag': options.hin_options.fc_flag,
           'CbFlag': options.hin_options.cb_flag,
           'AbsFlag': options.hin_options.abs_flag,
           'useSP': options.pin_options.use_spline,
           'Ecutoff': mol.energy_cutoff
           },
        '%(fH0)s \n'
        % {'fH0': paths.run_data + '/' + files.radial_ham},
        '%(fH0gm)s \n'
        % {'fH0gm': paths.run_data + '/' + files.angular_ham},
        '%(mass1)f %(re1)f %(ndvr1)d\n'
        % {'mass1': mol.lr.mass,
           're1': mol.lr.length[2],
           'ndvr1': mol.lr.num_dvr_fns
           },
        '%(psovbr_lr)s \n'
        % {'psovbr_lr': paths.run_data + '/' + files.psovbr_lr},
        '%(mass2)f %(re2)f %(ndvr2)d\n'
        % {'mass2': mol.br.mass,
           're2': mol.br.length[2],
           'ndvr2': mol.br.num_dvr_fns
           },
        '%(psovbr_br)s \n'
        % {'psovbr_br': paths.run_data + '/' + files.psovbr_br},
        '%(ndvr)d %(reFlag)d\n'
        % {'ndvr': options.hin_options.num_res_angles,
           'reFlag': options.in_switches.s_equil_r
           }
    ]
    if options.in_switches.s_equil_r == "T":
        hin_file.append('%(f_equil_r)s \n'
                        % {'f_equil_r': paths.run_data + '/' + options.in_switches.f_equil_r})
    if options.pin_options.use_spline == "T":
        hin_file.append(paths.pes_data + '/' + files.psovbr_lr + '\n')
        hin_file.append(paths.pes_data + '/' + files.psovbr_br)
    fh = open(name=paths.run + '/' + files.hamiltonian + files.input, mode='w')
    fh.write("".join(hin_file))
    fh.close()
    print '    File Generated: ' + paths.run + '/' + files.hamiltonian + files.input


def step_three(paths, files, mol, options):
    """

    :param paths:
    :param files:
    :param mol:
    :param options:
    :return:
    """
    #  Do we use max_angle value?

    #  Create List of Each Line of Third Step Input File
    in_file = [
        '%(sF)d %(lr)d %(br)d %(gm)d\n'
        % {'sF': options.in_options.s_f,
           'lr': mol.lr.num_dvr_fns,
           'br': mol.br.num_dvr_fns,
           'gm': min(options.hin_options.num_res_angles, mol.jk_num)
           },
        '%(sDep_lr)s %(sDep_br)s %(sDep_gm)s\n'
        % {'sDep_lr': options.in_switches.s_dep[0],
           'sDep_br': options.in_switches.s_dep[1],
           'sDep_gm': options.in_switches.s_dep[2]
           },
        '%(sJOB)d %(sOSB)d\n'
        % {'sJOB': options.in_options.s_job,
           'sOSB': options.in_options.s_osb
           },
        '%(sCX)s %(sNDVR)s %(sST)s %(sAP)s\n'
        % {'sCX': options.in_options.s_cx,
           'sNDVR': options.in_options.s_ndvr,
           'sST': options.in_options.s_st,
           'sAP': options.in_switches.s_ap
           },
        '%(BJ_iters)d %(BJ_tol)f %(QMR_iters)d %(QMR_tol)f\n'
        % {'BJ_iters': options.in_options.bj_num_iters,
           'BJ_tol': options.in_options.bj_tolerance,
           'QMR_iters': options.in_options.qmr_num_iters,
           'QMR_tol': options.in_options.qmr_tolerance
           },
        '%(pist_e0)f %(lanc_tol)f %(lanc_start)d %(lanc_step)d %(lanc_max)d %(lanc_num_eig)d %(lanc_gap)d\n'
        % {'pist_e0': options.in_options.pist_e0,
           'lanc_tol': options.in_options.pist_lanc_tolerance,
           'lanc_start': options.in_options.pist_start,
           'lanc_step': options.in_options.pist_step,
           'lanc_max': options.in_options.pist_max,
           'lanc_num_eig': options.in_options.pist_num_e0,
           'lanc_gap': options.in_options.pist_gap
           },
        '%(osb_e0)f %(osb_de)f %(osb_beta)f %(osb_count)d\n'
        % {'osb_e0': options.in_options.osb_e0,
           'osb_de': options.in_options.osb_de,
           'osb_beta': options.in_options.osb_beta,
           'osb_count': options.in_options.osb_count
           },
        '%(s_hosb)d %(s_vosb)d %(s_hw)d %(s_vx)d %(s_pt)d\n'
        % {'s_hosb': options.in_switches.s_hosb,
           's_vosb': options.in_switches.s_vosb,
           's_hw': options.in_switches.s_hw,
           's_vx': options.in_switches.s_vx,
           's_pt': options.in_switches.s_pt
           },
        '%(fH0)s\n'
        % {'fH0': paths.run_data + '/' + files.radial_ham},
        '%(fH0gm)s\n'
        % {'fH0gm': paths.run_data + '/' + files.angular_ham}
    ]

    #  Check Switches and Place Respective Files
    if options.in_switches.s_dep[0] == 'T':
        in_file.append(options.in_switches.f_dep[0] + '\n')
    if options.in_switches.s_dep[1] == 'T':
        in_file.append(options.in_switches.f_dep[1] + '\n')
    if options.in_switches.s_dep[2] == 'T':
        in_file.append(options.in_switches.f_dep[2] + '\n')
    if options.in_switches.s_ap == 'T':
        in_file.append(options.in_switches.f_app + '\n')
        in_file.append(options.in_switches.f_apr + '\n')
    if options.in_switches.s_hosb != '0':
        in_file.append(options.in_switches.f_hosb + '\n')
    if options.in_switches.s_vosb != '0':
        in_file.append(options.in_switches.f_vosb + '\n')
        in_file.append(options.in_switches.f_eig + '\n')
    if options.in_switches.s_hw != '0':
        in_file.append(options.in_switches.f_hw + '\n')
    if options.in_switches.s_vx != '0':
        in_file.append(options.in_switches.f_vx + '\n')
    if options.in_switches.s_pt != '0':
        in_file.append(options.in_switches.f_pt + '\n')

    #  Write Out List To File
    fh = open(paths.run + '/' + files.iterate + files.input, mode='w')
    fh.write("".join(in_file))
    fh.close()
    print '    File Generated: ' + paths.run + '/' + files.iterate + files.input
