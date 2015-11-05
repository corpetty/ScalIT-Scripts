__author__ = 'Corey Petty'
import triatomic.molecule as molecule
import triatomic.environment as environment
import triatomic.options as options
import util.environment as mpi_env


def create_class(params):
    """

    :param params:
    :type params: dict
    :returns: paths, mol, opts
    :rtype: Options()
    """
    # Transfer Params variables to directories class
    work_dir = params['dirs']['work']
    data_dir = params['dirs']['data']
    scalit_dir = params['dirs']['scalit']
    paths = environment.Directories(work=work_dir, data=data_dir, scalit=scalit_dir)

    # Transfer Params variables to Molecule class
    name = params['mol']['Name']
    mass_combo = params['mol']['mass_opt']
    j_total = params['hin_opts']['j_total']
    j_max = params['hin_opts']['jmax']
    permutation = params['hin_opts']['permutation']
    parity = params['hin_opts']['parity']
    energy_cutoff = params['hin_opts']['Ecutoff']
    mass = params['mol']['mass']
    lr_length = (params['mol']['Rmin'][0], params['mol']['Rmax'][0], params['mol']['re'][0])
    br_length = (params['mol']['Rmin'][1], params['mol']['Rmax'][1], params['mol']['re'][1])
    num_sinc_fns = params['pin_opts']['num_sinc_fns']
    num_vbr_fns = params['pin_opts']['max_DVR_fns']
    num_lr_dvr_fns = params['hin_opts']['num_lr_functions']
    num_br_dvr_fns = params['hin_opts']['num_Br_functions']
    mol = molecule.Molecule(name=name, mass_combo=mass_combo, j_total=j_total, j_max=j_max, permutation=permutation,
                            parity=parity, energy_cutoff=energy_cutoff, mass=mass, lr_length=lr_length,
                            br_length=br_length, num_sinc_fns=num_sinc_fns, num_vbr_fns=num_vbr_fns,
                            num_lr_dvr_fns=num_lr_dvr_fns, num_br_dvr_fns=num_br_dvr_fns)

    # Transfer Params variables to Options class
    dvr_type = params['pin_opts']['dvr_type']
    use_spline = params['pin_opts']['useSP']
    restrict_num_angles = params['hin_opts']['restrict_num_angles']
    num_res_angles = params['hin_opts']['num_angles']
    ngi = params['hin_opts']['ngi']
    fc_flag = params['hin_opts']['FcFlag']
    cb_flag = params['hin_opts']['CbFlag']
    abs_flag = params['hin_opts']['AbsFlag']
    s_equil_r = params['hin_opts']['ReFlag']
    s_f = params['in_opts']['sF']
    s_dep = params['in_opts']['sDep']
    s_job = params['in_opts']['sJOB']
    s_osb = params['in_opts']['sOSB']
    s_cx = params['in_opts']['sCX']
    s_ndvr = params['in_opts']['sNDVR']
    s_st = params['in_opts']['sST']
    s_ap = params['in_opts']['sAP']
    s_hosb = params['in_opts']['sHOSB']
    s_vosb = params['in_opts']['sVOSB']
    s_hw = params['in_opts']['sHW']
    s_vx = params['in_opts']['sVX']
    s_pt = params['in_opts']['sPT']
    f_equil_r = params['in_file_names']['fRES']
    f_dep = params['in_file_names']['fDep']
    f_ap = params['in_file_names']['fAPP']
    f_apr = params['in_file_names']['fAPR']
    f_hosb = params['in_file_names']['fHOSB']
    f_vosb = params['in_file_names']['fVOSB']
    f_eig = params['in_file_names']['fEig']
    f_hw = params['in_file_names']['fHW']
    f_vx = params['in_file_names']['fVX']
    f_pt = params['in_file_names']['fPT']

    opts = options.Options(dvr_type=dvr_type, use_spline=use_spline, restrict_num_angles=restrict_num_angles,
                           num_res_angles=num_res_angles, ngi=ngi, fc_flag=fc_flag, cb_flag=cb_flag, abs_flag=abs_flag,
                           s_f=s_f, s_job=s_job, s_osb=s_osb, s_cx=s_cx, s_ndvr=s_ndvr, s_st=s_st,
                           s_equil_r=s_equil_r, f_equil_r=f_equil_r, s_dep=s_dep, f_dep=f_dep,
                           s_ap=s_ap, f_ap=f_ap, f_apr=f_apr, s_hosb=s_hosb, f_hosb=f_hosb,
                           s_vosb=s_vosb, f_vosb=f_vosb, f_eig=f_eig, s_hw=s_hw, f_hw=f_hw,
                           s_vx=s_vx, f_vx=f_vx, s_pt=s_pt, f_pt=f_pt)

    # Transfer Paramss variables to Mpi class
    if params['run_opts']['version'] != 0:
        use_mpi = True
    else:
        use_mpi = False

    platform = params['dirs']['host']
    if platform == ('Robinson' or 'Lonestar' or 'Hrothgar'):
        use_sge = True
    else:
        use_sge = False

    local_cores = params['run_opts']['local_cores']
    nodes_desired = params['run_opts']['nodes_desired']
    run_time = params['run_opts']['run_time']

    mpi = mpi_env.Mpi(use_mpi=use_mpi, use_sge=use_sge, platform=platform, cores=local_cores,
                      nodes_desired=nodes_desired, runtime=run_time)

    return paths, mol, opts, mpi
