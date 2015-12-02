__author__ = 'Corey Petty'


class Options(object):
    def __init__(self,
                 dvr_type=2, restrict_num_angles="F", num_res_angles=0, ngi=300, fc_flag=0,
                 cb_flag=0, abs_flag=0, s_f=3, s_job=1, s_osb=0, s_cx='F', s_ndvr='T', s_st='T',
                 bj_num_iters=10, bj_tolerance=1.0E-3, qmr_num_iters=10000, qmr_tolerance=1.0E-3, pist_e0=0.0,
                 pist_lanc_tolerance=1.0E-9, pist_start=50, pist_step=10, pist_max=400, pist_num_e0=30, pist_gap=5,
                 osb_e0=0.0, osb_de=1.0E-3, osb_beta=1.0, osb_count=1000,
                 s_equil_r=0, f_equil_r='fRES.dat',
                 s_dep=('F', 'F', 'F'), f_dep=('fDep1.dat', 'fDep2.dat', 'fDep3.dat'),
                 s_ap='F', f_ap='fAPP.dat', f_apr='fAPR.dat',
                 f_eig='fEig.dat',
                 s_hosb=0, f_hosb='fHOSB.dat',
                 s_vosb=0, f_vosb='fVOSB.dat',
                 s_hw=0, f_hw='fHW.dat',
                 s_vx=0, f_vx='fVX.dat',
                 s_pt=0, f_pt='fPT.dat',
                 k_num=-1, g_type=True, s_type=False, num_states=-1,
                 lr_plotpoints=10, br_plotpoints=10, angle_plotpoints=10
                 ):
        self.pin_options = self.PinOptions(dvr_type=dvr_type)
        self.hin_options = self.HinOptions(restrict_num_angles=restrict_num_angles, num_res_angles=num_res_angles,
                                           ngi=ngi, fc_flag=fc_flag, cb_flag=cb_flag, abs_flag=abs_flag)
        self.in_options = self.InOptions(s_f=s_f, s_job=s_job, s_osb=s_osb, s_cx=s_cx, s_ndvr=s_ndvr,
                                         s_st=s_st,
                                         bj_num_iters=bj_num_iters,
                                         bj_tolerance=bj_tolerance,
                                         qmr_num_iters=qmr_num_iters,
                                         qmr_tolerance=qmr_tolerance,
                                         pist_e0=pist_e0,
                                         pist_lanc_tolerance=pist_lanc_tolerance,
                                         pist_start=pist_start,
                                         pist_step=pist_step,
                                         pist_max=pist_max,
                                         pist_num_e0=pist_num_e0,
                                         pist_gap=pist_gap,
                                         osb_e0=osb_e0,
                                         osb_de=osb_de,
                                         osb_beta=osb_beta,
                                         osb_count=osb_count)
        self.in_switches = self.InSwitches(s_equil_r=s_equil_r, f_equil_r=f_equil_r, s_dep=s_dep, f_dep=f_dep,
                                           s_ap=s_ap, f_ap=f_ap, f_apr=f_apr, s_hosb=s_hosb, f_hosb=f_hosb,
                                           s_vosb=s_vosb, f_vosb=f_vosb, f_eig=f_eig, s_hw=s_hw, f_hw=f_hw,
                                           s_vx=s_vx, f_vx=f_vx, s_pt=s_pt, f_pt=f_pt)
        self.sin_options = self.SinOptions(k_num=k_num, g_type=g_type, s_type=s_type, num_states=num_states,
                                           lr_plotpoints=lr_plotpoints, br_plotpoints=br_plotpoints,
                                           angle_plotpoints=angle_plotpoints)

    class PinOptions(object):
        def __init__(self,
                     dvr_type=2
                     ):
            self.dvr_type = dvr_type

    class HinOptions(object):
        def __init__(self,
                     restrict_num_angles="F", num_res_angles=0, ngi=300,
                     fc_flag=0, cb_flag=0, abs_flag=0
                     ):
            self.restrict_num_angles = restrict_num_angles
            self.num_res_angles = num_res_angles
            self.ngi = ngi
            self.fc_flag = fc_flag
            self.cb_flag = cb_flag
            self.abs_flag = abs_flag

    class InOptions(object):
        def __init__(self,
                     s_f=3, s_job=1, s_osb=0,
                     s_cx='F', s_ndvr='T', s_st='T',
                     bj_num_iters=10,
                     bj_tolerance=1.0E-3,
                     qmr_num_iters=10000,
                     qmr_tolerance=1.0E-3,
                     pist_e0=0.0,
                     pist_lanc_tolerance=1.0E-9,
                     pist_start=50,
                     pist_step=10,
                     pist_max=400,
                     pist_num_e0=30,
                     pist_gap=5,
                     osb_e0=0.0,
                     osb_de=1.0E-3,
                     osb_beta=1.0,
                     osb_count=1000
                     ):
            self.s_f = s_f
            self.s_job = s_job
            self.s_osb = s_osb
            self.s_cx = s_cx
            self.s_ndvr = s_ndvr
            self.s_st = s_st
            self.bj_num_iters = bj_num_iters
            self.bj_tolerance = bj_tolerance
            self.qmr_num_iters = qmr_num_iters
            self.qmr_tolerance = qmr_tolerance
            self.pist_e0 = pist_e0
            self.pist_lanc_tolerance = pist_lanc_tolerance
            self.pist_start = pist_start
            self.pist_step = pist_step
            self.pist_max = pist_max
            self.pist_num_e0 = pist_num_e0
            self.pist_gap = pist_gap
            self.osb_e0 = osb_e0
            self.osb_de = osb_de
            self.osb_beta = osb_beta
            self.osb_count = osb_count

    #  TODO: move s_equil_r to hin_opts and change to True
    class InSwitches(object):
        def __init__(self,
                     s_equil_r=0, f_equil_r='fRES.dat',
                     s_dep=('F', 'F', 'F'), f_dep=('fDep1.dat', 'fDep2.dat', 'fDep3.dat'),
                     s_ap='F', f_ap='fAPP.dat',
                     f_apr='fAPR.dat',
                     s_hosb=0, f_hosb='fHOSB.dat',
                     s_vosb=0, f_vosb='fVOSB.dat',
                     f_eig='fEig.dat',
                     s_hw=0, f_hw='fHW.dat',
                     s_vx=0, f_vx='fVX.dat',
                     s_pt=0, f_pt='fPT.dat'
                     ):
            self.s_equil_r = s_equil_r
            self.f_equil_r = f_equil_r
            self.s_dep = s_dep
            self.f_dep = f_dep
            self.s_ap = s_ap
            self.f_ap = f_ap
            self.f_apr = f_apr
            self.s_hosb = s_hosb
            self.f_hosb = f_hosb
            self.s_vosb = s_vosb
            self.f_vosb = f_vosb
            self.f_eig = f_eig
            self.s_hw = s_hw
            self.f_hw = f_hw
            self.s_vx = s_vx
            self.f_vx = f_vx
            self.s_pt = s_pt
            self.f_pt = f_pt

    class SinOptions(object):
        def __init__(self,
                     k_num=-1, g_type=True, s_type=False, num_states=-1,
                     lr_plotpoints=10, br_plotpoints=10, angle_plotpoints=10):
            self.k_num = k_num
            self.g_type = g_type
            self.s_type = s_type
            self.num_states = num_states
            self.lr_plotpoints = lr_plotpoints
            self.br_plotpoints = br_plotpoints
            self.angle_plotpoints = angle_plotpoints
