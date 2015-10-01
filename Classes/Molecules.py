__author__ = 'Corey Petty'


class Molecule(object):
    """
    Class object that defines all parameters for a Triatomic Molecule.
    """
    num_radial_coords = 2

    def __init__(self, mass_combo, j_total, j_max, permutation, parity):
        self.mass_combo = mass_combo
        self.j_total = j_total
        self.j_max = j_max
        self.jk_num = 0
        self.permutation = permutation
        self.parity = parity
        self.energy_cutoff = 1
        self.lr = self.RadialCoordinate()
        self.br = self.RadialCoordinate()

    class RadialCoordinate(object):
        def __init__(self):
            self.mass = 0.0
            self.min_length = 0.0
            self.max_length = 10.0
            self.eq_length = 5.0
            self.num_sinc_fns = 6000    # default
            self.num_vbr_fns = 100      # default
            self.num_dvr_fns = 30

    def get_num_angles(self):
        if self.permutation == 'even':
            if self.parity == 'even':
                jp = 0
            elif self.parity == 'odd':
                jp = 1
            else:
                print 'Incorrect parity option, choose (even,odd)'
                return 0
            jt = self.j_total + jp

            if jt / 2 * 2 == jt:
                k_min = 0
            else:
                k_min = 1

            self.jk_num = 0
            for j in range(0, self.j_max + 1):
                k_max = min(self.j_total, j)
                for k in range(k_min, k_max + 1):
                    jk = j + jp
                    if jk / 2 * 2 == jk:
                        self.jk_num += 1
        elif self.permutation == 'odd':  # even permutation
            if self.parity == 'even':  # even parity
                jp = 0
            elif self.parity == 'odd':  # odd parity
                jp = 1
            else:
                print 'Incorrect parity option, choose (even,odd)'
                return 0
            jt = self.j_total + jp  # total parity = (-1)^(p+JTol)

            if jt == jt / 2 * 2:  # even total parity
                k_min = 0
            else:
                k_min = 1
            self.jk_num = 0
            for j in range(0, self.j_max + 1):
                k_max = min(self.j_total, j)
                for k in range(k_min, k_max + 1):
                    jk = j + jp
                    if jk / 2 * 2 != jk:
                        self.jk_num += 1
        else:
            print 'Incorrect permutation option, choose (even,odd)'
