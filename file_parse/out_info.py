__author__ = 'Corey Petty'
import datetime


def get_eigenvalues(outfile: str) -> list:
    eig_list = []
    with open(outfile, mode='r') as f:
        for num, line in enumerate(f, 1):
            if "Max Lanczos" in line:
                break
        for line in f:
            if "---" in line:
                break
            for eig in line.split():
                eig_list.append(float(eig))
    # print("The eigenvalues are:")
    # for eig in eig_list:
    #     print('\t{:E}'.format(eig))
    return eig_list


def total_runtime_out(outfile: str) -> list:
    time_list = []
    with open(outfile, mode='r') as f:
        for line in f:
            if "Time" in line and "MPI_WTime" not in line:
                # print(line)
                time_list.append(float(line.split()[-1]))
        # print("Total time of program: \n\t%(sec)f seconds \n\t%(min)f minutes \n\t%(hr)f hours"
        #       % {'sec': sum(time_list),
        #          'min': sum(time_list) / 60,
        #          'hr': sum(time_list) / 3600
        #          })
        for num, time in enumerate(time_list):
            time_list[num] = datetime.timedelta(seconds=time)
    return time_list


def get_lanczos_error(outfile: str) -> str:
    return_string = "Lanczos Error not found, job may be running or encountered an error. \n" + \
                    "  see file {}".format(outfile)
    with open(outfile, mode='r') as f:
        for line in f:
            if "Max Lanczos" in line:
                return_string = "{}".format(line.split()[3])
    return return_string


def get_central_energy(outfilename: str) -> float:
    central_energy = 0.0
    with open(outfilename, mode='r') as outfile:
        for line in outfile:
            if "Central Energy:" in line:
                central_energy = float(line.split()[-1])
    return central_energy
