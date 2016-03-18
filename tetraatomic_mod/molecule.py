__author__ = 'Corey Petty'


#  TODO:  provide potential energy units
class Molecule(object):
    """
    Class object that defines all parameters for a Tetra-atomic Molecule.
    """
    num_radial_coords = 3

    def __init__(self, name="", mass_combo="", j_total=0, j1_max=0, j2_max=0, permutation='Agg',
                 parity='even', energy_cutoff=1, mass=(0.0, 0.0, 0.0),
                 lr1_length=(0.0, 10.0, 5.0), lr2_length=(0,0, 10.0, 5.0), br_length=(0.0, 10.0, 5.0),
                 num_sinc_fns=6000, num_vbr_fns=100,
                 num_lr1_dvr_fns=30, num_lr2_dvr_fns=30, num_br_dvr_fns=30,
                 use_spline=True):
        self.name = name
        self.mass_combo = mass_combo
        self.j_total = j_total
        self.j1_max = j1_max
        self.j2_max = j2_max
        self.j12_max = self.j1_max + self.j2_max
        self.permutation = permutation
        self.parity = parity
        self.energy_cutoff = energy_cutoff
        self.lr1 = self.RadialCoordinate(mass[0], lr1_length, num_sinc_fns, num_vbr_fns, num_lr1_dvr_fns, suffix="lr1")
        self.lr2 = self.RadialCoordinate(mass[1], lr2_length, num_sinc_fns, num_vbr_fns, num_lr2_dvr_fns, suffix="lr2")
        self.br = self.RadialCoordinate(mass[2], br_length, num_sinc_fns, num_vbr_fns, num_br_dvr_fns, suffix="BR")
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
        if self.permutation == "Agg":
            for j1 in range(0, self.j1_max + 1, 2):
                for j2 in range(0, self.j2_max + 1, 2):
                    j0_min = abs(j1 - j2)
                    j0_max = min(j1 + j2, self.j12_max)
                    for j in range(j0_min, j0_max + 1):
                        k0_max = min(j, self.j_total)
                        j_sum = j1 + j2 + j + self.j_total
                        if not self.parity:
                            j_sum += 1
                        if j_sum % 2 == 0:
                            k_min = 0
                        else:
                            k_min = 1
                        self.jk_num = self.jk_num + k0_max + 1 - k_min
        elif self.permutation == "Auu":
            for j1 in range(1, self.j1_max + 1, 2):
                for j2 in range(1, self.j2_max + 1, 2):
                    j0_min = abs(j1 - j2)
                    j0_max = min(j1 + j2, self.j12_max)
                    for j in range(j0_min, j0_max + 1):
                        k0_max = min(j, self.j_total)
                        j_sum = j1 + j2 + j + self.j_total
                        if not self.parity:
                            j_sum += 1
                        if j_sum % 2 == 0:
                            k_min = 0
                        else:
                            k_min = 1
                        self.jk_num = self.jk_num + k0_max + 1 - k_min
        elif self.permutation == "Agu":
            for j1 in range(0, self.j1_max + 1, 2):
                for j2 in range(1, self.j2_max + 1, 2):
                    j0_min = abs(j1 - j2)
                    j0_max = min(j1 + j2, self.j12_max)
                    for j in range(j0_min, j0_max + 1):
                        k0_max = min(j, self.j_total)
                        j_sum = j1 + j2 + j + self.j_total
                        if not self.parity:
                            j_sum += 1
                        if j_sum % 2 == 0:
                            k_min = 0
                        else:
                            k_min = 1
                        self.jk_num = self.jk_num + k0_max + 1 - k_min
        elif self.permutation == "Aug":
            for j1 in range(1, self.j1_max + 1, 2):
                for j2 in range(0, self.j2_max + 1, 2):
                    j0_min = abs(j1 - j2)
                    j0_max = min(j1 + j2, self.j12_max)
                    for j in range(j0_min, j0_max + 1):
                        k0_max = min(j, self.j_total)
                        j_sum = j1 + j2 + j + self.j_total
                        if not self.parity:
                            j_sum += 1
                        if j_sum % 2 == 0:
                            k_min = 0
                        else:
                            k_min = 1
                        self.jk_num = self.jk_num + k0_max + 1 - k_min
        else:
            print("You've chose an incorrect permutation:"
                  "    options include:"
                  "         Agg"
                  "         Auu"
                  "         Agu"
                  "         Aug")
            return 0

    def print_jknum(self):
        print('\n')
        print('----> Calculating number of possible angles: ')
        print('    J total:      ' + str(self.j_total))
        print('    j1 max:       ' + str(self.j1_max))
        print('    j2 max:       ' + str(self.j2_max))
        print('    j12 max:      ' + str(self.j12_max))
        print('    permutation:  ' + self.permutation)
        print('    parity:       ' + self.parity + '\n')
        print('    Number of possible angles (jk_num): ' + str(self.jk_num) + '\n')
