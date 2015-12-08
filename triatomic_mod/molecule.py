__author__ = 'Corey Petty'


#  TODO:  provide potential energy units
class Molecule(object):
    """
    Class object that defines all parameters for a Triatomic Molecule.
    """
    num_radial_coords = 2

    def __init__(self, name="", mass_combo="", j_total=0, j_max=0, permutation='even',
                 parity='even', energy_cutoff=1, mass=(0.0, 0.0),
                 lr_length=(0.0, 10.0, 5.0), br_length=(0.0, 10.0, 5.0),
                 num_sinc_fns=6000, num_vbr_fns=100,
                 num_lr_dvr_fns=30, num_br_dvr_fns=30,
                 use_spline=True):
        self.name = name
        self.mass_combo = mass_combo
        self.j_total = j_total
        self.j_max = j_max
        self.permutation = permutation
        self.parity = parity
        self.energy_cutoff = energy_cutoff
        self.lr = self.RadialCoordinate(mass[0], lr_length, num_sinc_fns, num_vbr_fns, num_lr_dvr_fns, suffix="lr")
        self.br = self.RadialCoordinate(mass[1], br_length, num_sinc_fns, num_vbr_fns, num_br_dvr_fns, suffix="BR")
        self.jk_num = None
        self.get_num_angles()
        self.use_spline = use_spline

    class RadialCoordinate(object):
        def __init__(self, mass=0.0, length=(0.0, 10.0, 5.0), num_sinc_fns=6000, num_vbr_fns=100, num_dvr_fns=30,
                     suffix=""):
            self.mass = mass
            self.length = length                  # Given as (min, max, equilibrium)
            self.num_sinc_fns = num_sinc_fns
            self.num_vbr_fns = num_vbr_fns
            self.num_dvr_fns = num_dvr_fns
            self.suffix = suffix

    def get_num_angles(self):
        if self.permutation == ('even' or 'Even' or 'T' or True):
            if self.parity == ('even' or 'Even' or 'T' or True):
                jp = 0
            elif self.parity == ('odd' or 'Odd' or 'F' or False):
                jp = 1
            else:
                print('Incorrect parity option, choose (even,odd)')
                return 0
            jt = self.j_total + jp
            if jt % 2 == 0:
                k_min = 0
            else:
                k_min = 1
            self.jk_num = 0
            for j in range(0, self.j_max + 1):
                k_max = min(self.j_total, j)
                for _ in range(k_min, k_max + 1):
                    jk = j + jp
                    if jk % 2 == 0:
                        self.jk_num += 1
        elif self.permutation == ('odd' or 'Odd' or 'F' or False):  # even permutation
            if self.parity == ('even' or 'Even' or 'T' or True):  # even parity
                jp = 0
            elif self.parity == ('odd' or 'Odd' or 'F' or False):  # odd parity
                jp = 1
            else:
                print('Incorrect parity option, choose (even,odd)')
                return 0
            jt = self.j_total + jp  # total parity = (-1)^(p+JTol)
            if jt % 2 == 0:  # even total parity
                k_min = 0
            else:
                k_min = 1
            self.jk_num = 0
            for j in range(0, self.j_max + 1):
                k_max = min(self.j_total, j)
                for _ in range(k_min, k_max + 1):
                    jk = j + jp
                    if jk % 2 != 0:
                        self.jk_num += 1
        else:
            print('Incorrect permutation option, choose (even,odd)')
            return 0

    def print_jknum(self):
        print('\n')
        print('----> Calculating number of possible angles: ')
        print('    J total:      ' + str(self.j_total))
        print('    j max:        ' + str(self.j_max))
        print('    permutation:  ' + self.permutation)
        print('    parity:       ' + self.parity + '\n')
        print('    Number of possible angles (jk_num): ' + str(self.jk_num) + '\n')
