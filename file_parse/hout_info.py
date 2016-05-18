__author__ = 'Corey Petty'
import datetime


def get_total_runtime(houtfile: str) -> (datetime.datetime, datetime.datetime):
    mpi_time = 0
    cpu_time = 0
    with open(houtfile, mode='r') as f:
        for line in f:
            if 'MPI Time' in line:
                time_flt = float(line.split()[-1])
                mpi_time = datetime.timedelta(seconds=time_flt)
            if 'CPU Time for the program' in line:
                time_flt = float(line.split()[-1])
                cpu_time = datetime.timedelta(seconds=time_flt)
    return mpi_time, cpu_time


def get_num_cores(houtfilename: str) -> int:
    """
    Function to parse a hamiltonian creation output file and return number of cores used in job
    returns 1 if the serial executable is used
    """
    counter = 0
    with open(houtfilename, mode='r') as houtfile:
        for line in houtfile:
            if 'range of index' in line:
                counter += 1
    if counter == 0:
        return 1
    else:
        return counter


def get_parity(houtfilename: str) -> str:
    parity = ''
    with open(houtfilename, mode='r') as houtfile:
        for line in houtfile:
            if 'JTol' in line:
                parity = line.split()[4]
    if parity == 'T':
        parity = 'even'
    else:
        parity = 'odd'
    return parity


def break_apart_path(houtfilename: str) -> (str, str, int, str):
    name, mass_option, j, permutation = '', '', 0, ''
    with open(houtfilename, mode='r') as houtfile:
        for line in houtfile:
            if 'Filename to store H0' in line:
                name, mass_option, j, permutation, _ = line.split('/')[-5:]
    j = j[1:]
    return name, mass_option, j, permutation


def get_basis_size(houtfilename: str) -> (int, int, int, int):
    num_lr, num_br, num_jmax, num_gm = 0, 0, 0, 0
    lr_break = 0  # flag to stop at first get
    br_break = 0  # flag to stop at first get
    with open(houtfilename, mode='r') as houtfile:
        for line in houtfile:
            if 'lr:' in line and lr_break == 0:
                num_lr = line.split()[2]
                lr_break = 1  # no more assignments
            if 'BR:' in line and br_break == 0:
                num_br = line.split()[2]
                br_break = 1  # no more assignments
            if '# of (jk)' in line:
                num_gm = line.split()[4]
            if 'jmax:' in line:
                num_jmax = line.split()[5]
    return num_lr, num_br, num_jmax, num_gm
