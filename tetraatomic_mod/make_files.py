__author__ = 'Corey Petty'


def step_one(paths, files, molecule, pin_options):
    """

    :param paths:
    :param files:
    :param molecule:
    :param pin_options:
    :return:
    """
    #  Little r1
    #    Create file substance, line by line
    line_one = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
               % {'type': pin_options.dvr_type,
                  'mass': molecule.lr1.mass,
                  'nmax': molecule.lr1.num_sinc_fns,
                  'nmin': molecule.lr1.num_vbr_fns,
                  'useSP': 'T' if molecule.use_spline else 'F'
                  }
    line_two = '%(Rmin)f %(Rmax)f\n' \
               % {'Rmin': molecule.lr1.length[0],
                  'Rmax': molecule.lr1.length[1]
                  }

    line_three = '%(outfile)s' \
                 % {'outfile': paths.run_psovbr_data + '/' + files.psovbr_lr1}

    #    Write the files
    fh = open(paths.run_psovbr + '/' + files.presinc_lr1 + files.input, 'w')
    fh.write(line_one + line_two + line_three)
    if molecule.use_spline:
        fh.write('\n' + paths.pes_data + '/' + files.v_eff_lr1)
    fh.close()
    print('    File Generated: ' + paths.run_psovbr + '/' + files.presinc_lr1 + files.input)

    #  Little r2
    #    Create file substance, line by line
    line_one = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
               % {'type': pin_options.dvr_type,
                  'mass': molecule.lr2.mass,
                  'nmax': molecule.lr2.num_sinc_fns,
                  'nmin': molecule.lr2.num_vbr_fns,
                  'useSP': 'T' if molecule.use_spline else 'F'
                  }
    line_two = '%(Rmin)f %(Rmax)f\n' \
               % {'Rmin': molecule.lr2.length[0],
                  'Rmax': molecule.lr2.length[1]
                  }

    line_three = '%(outfile)s' \
                 % {'outfile': paths.run_psovbr_data + '/' + files.psovbr_lr2}

    #    Write the files
    fh = open(paths.run_psovbr + '/' + files.presinc_lr2 + files.input, 'w')
    fh.write(line_one + line_two + line_three)
    if molecule.use_spline:
        fh.write('\n' + paths.pes_data + '/' + files.v_eff_lr2)
    fh.close()
    print('    File Generated: ' + paths.run_psovbr + '/' + files.presinc_lr2 + files.input)

    #  Big R
    #    Create file substance, line by line
    line_one = '%(type)d %(mass)f %(nmax)d %(nmin)d %(useSP)s \n' \
               % {'type': pin_options.dvr_type,
                  'mass': molecule.br.mass,
                  'nmax': molecule.br.num_sinc_fns,
                  'nmin': molecule.br.num_vbr_fns,
                  'useSP': 'T' if molecule.use_spline else 'F'
                  }
    line_two = '%(Rmin)f %(Rmax)f\n' \
               % {'Rmin': molecule.br.length[0],
                  'Rmax': molecule.br.length[1]
                  }

    line_three = '%(outfile)s' \
                 % {'outfile': paths.run_psovbr_data + '/' + files.psovbr_br}

    #    Write the files
    fh = open(paths.run_psovbr + '/' + files.presinc_br + files.input, 'w')
    fh.write(line_one + line_two + line_three)
    if molecule.use_spline:
        fh.write('\n' + paths.pes_data + '/' + files.v_eff_br)
    fh.close()
    print('    File Generated: ' + paths.run_psovbr + '/' + files.presinc_br + files.input)


def step_two(paths, files, molecule, options):
    """
    Creates the Step Two (Hamiltonian Constructrion) input files.  Requires
    the following class instances.
    :param paths:
    :param files:
    :param molecule:
    :param options:
    :return:
    """

    hin_file = ['%(jtol)d %(parity)s '
                % {'jtol': molecule.j_total,
                   'parity': 'F' if molecule.parity == 'odd' else 'T'
                   },
                '%(j1max)d %(j2max)d %(j12max)d %(ngi1)d %(ngi2)d %(ngi12)d\n'
                % {'j1max': molecule.j1_max,
                   'j2max': molecule.j2_max,
                   'j12max': molecule.j12_max,
                   'ngi1': options.hin_options.ngi1,
                   'ngi2': options.hin_options.ngi2,
                   'ngi12': options.hin_options.ngi12
                   },
                '%(FcFlag)d %(CbFlag)d %(AbsFlag)d %(useSP)s %(Ecutoff)f\n'
                % {'FcFlag': options.hin_options.fc_flag,
                   'CbFlag': options.hin_options.cb_flag,
                   'AbsFlag': options.hin_options.abs_flag,
                   'useSP': 'T' if molecule.use_spline else 'F',
                   'Ecutoff': molecule.energy_cutoff
                   },
                '%(fH0)s \n'
                % {'fH0': paths.run_data + '/' + files.radial_ham},
                '%(fH0gm)s \n'
                % {'fH0gm': paths.run_data + '/' + files.angular_ham},
                '%(mass1)f %(re1)f %(ndvr1)d\n'
                % {'mass1': molecule.lr1.mass,
                   're1': molecule.lr1.length[2],
                   'ndvr1': molecule.lr1.num_dvr_fns
                   },
                '%(psovbr_lr1)s \n'
                % {'psovbr_lr1': paths.run_psovbr_data + '/' + files.psovbr_lr1},
                '%(mass2)f %(re2)f %(ndvr2)d\n'
                % {'mass2': molecule.lr2.mass,
                   're2': molecule.lr2.length[2],
                   'ndvr2': molecule.lr2.num_dvr_fns
                   },
                '%(psovbr_lr2)s \n'
                % {'psovbr_lr2': paths.run_psovbr_data + '/' + files.psovbr_lr2},
                '%(mass2)f %(re2)f %(ndvr2)d\n'
                % {'mass2': molecule.br.mass,
                   're2': molecule.br.length[2],
                   'ndvr2': molecule.br.num_dvr_fns
                   },
                '%(psovbr_br)s \n'
                % {'psovbr_br': paths.run_psovbr_data + '/' + files.psovbr_br},
                '%(ndvr)d %(reFlag)d\n'
                % {'ndvr': options.hin_options.num_res_angles,
                   'reFlag': options.in_switches.s_equil_r
                   },
                '%(f_equil_r)s \n'
                % {'f_equil_r': paths.run_data + '/' + options.in_switches.f_equil_r}
                ]
    if molecule.use_spline:
        hin_file.append(paths.pes_data + '/' + files.v_eff_lr1 + '\n')
        hin_file.append(paths.pes_data + '/' + files.v_eff_lr2 + '\n')
        hin_file.append(paths.pes_data + '/' + files.v_eff_br)
    fh = open(paths.run + '/' + files.hamiltonian + files.input, 'w')
    fh.write("".join(hin_file))
    fh.close()
    print('    File Generated: ' + paths.run + '/' + files.hamiltonian + files.input)


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
        '%(sF)d %(lr1)d %(lr2)d %(br)d %(gm)d\n'
        % {'sF': options.in_options.s_f,
           'lr1': mol.lr1.num_dvr_fns,
           'lr2': mol.lr2.num_dvr_fns,
           'br': mol.br.num_dvr_fns,
           'gm': min(options.hin_options.num_res_angles, mol.jk_num)
           },
        '%(sDep_lr1)s %(sDep_lr2)s %(sDep_br)s %(sDep_gm)s\n'
        % {'sDep_lr1': options.in_switches.s_dep[0],
           'sDep_lr2': options.in_switches.s_dep[1],
           'sDep_br': options.in_switches.s_dep[2],
           'sDep_gm': options.in_switches.s_dep[3]
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
        '%(BJ_iters)d %(BJ_tol)g %(QMR_iters)d %(QMR_tol)g\n'
        % {'BJ_iters': options.in_options.bj_num_iters,
           'BJ_tol': options.in_options.bj_tolerance,
           'QMR_iters': options.in_options.qmr_num_iters,
           'QMR_tol': options.in_options.qmr_tolerance
           },
        '%(pist_e0)g %(lanc_tol)g %(lanc_start)d %(lanc_step)d %(lanc_max)d %(lanc_num_eig)d %(lanc_gap)d\n'
        % {'pist_e0': options.in_options.pist_e0,
           'lanc_tol': options.in_options.pist_lanc_tolerance,
           'lanc_start': options.in_options.pist_start,
           'lanc_step': options.in_options.pist_step,
           'lanc_max': options.in_options.pist_max,
           'lanc_num_eig': options.in_options.pist_num_e0,
           'lanc_gap': options.in_options.pist_gap
           },
        '%(osb_e0)g %(osb_de)g %(osb_beta)g %(osb_count)d\n'
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
    if options.in_switches.s_hosb != 0:
        in_file.append(options.in_switches.f_hosb + '\n')
    if options.in_switches.s_vosb != 0:
        in_file.append(options.in_switches.f_vosb + '\n')
        in_file.append(options.in_switches.f_eig + '\n')
    if options.in_switches.s_hw != 0:
        in_file.append(options.in_switches.f_hw + '\n')
    if options.in_switches.s_vx != 0:
        in_file.append(options.in_switches.f_vx + '\n')
    if options.in_switches.s_pt != 0:
        in_file.append(options.in_switches.f_pt + '\n')

    #  Write Out List To File
    fh = open(paths.run + '/' + files.iterate + files.input, 'w')
    fh.write("".join(in_file))
    fh.close()
    print('    File Generated: ' + paths.run + '/' + files.iterate + files.input)


def step_four(directories, files, molecule, options):
    """
    This part makes the wavefucntion input file for a ScalIT run.  Unlike the options,
    it will require some inputs from the user.

    NOTE: this does not work yet!!!!  Under Development!!!!

    Args:
        directories:
        files:
        molecule:
        options:

    Returns:

    """
    mass1 = input("Please input mass of atom 1 (amu): ")
    mass2 = input("Please input mass of atom 2 (amu): ")
    mass3 = input("Please input mass of atom 3 (amu): ")
    mass4 = input("Please input mass of atom 4 (amu): ")
    eig_index = input("Please input the indices of the states you want: ")
    sin_file = [
        '%(jtot)d %(parity)s\n'
        % {'jtot': molecule.j_total,
           'parity': 'e' if molecule.parity == 'even' else 'o'
           },
        '%(m1)f %(m2)f %(m3)f %(m3)f\n'
        % {'m1': mass1,
           'm2': mass2,
           'm3': mass3,
           'm4': mass4
           },
        '%(nState)d %(gType)s %(sType)s %(kNum)d\n'
        % {'nState': options.sin_options.num_states,
           'gType': options.sin_options.g_type,
           'sType': options.sin_options.s_type,
           'kNum': options.sin_options.k_num
           }
    ]
    if options.sin_options.num_states < 0:
        for index in eig_index:
            #  TODO: Fix this
            print(index)

    #  Write Out List To File
    with open(directories.run + '/' + files.wavefunction + files.input, 'w') as fh:
        fh.write("".join(sin_file))
        print('    File Generated: ' + directories.run + '/' + files.wavefunction + files.input)
