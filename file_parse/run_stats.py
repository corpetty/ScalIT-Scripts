__author__ = 'Corey Petty'


def total_runtime(outfile: str):
    time_list = []
    with open(outfile, mode='r') as f:
        for line in f:
            if "Time" in line and "MPI_WTime" not in line:
                print(line)
                time_list.append(float(line.split()[-1]))
        print("Total time of program: \n\t%(sec)f seconds \n\t%(min)f minutes \n\t%(hr)f hours"
              % {'sec': sum(time_list),
                 'min': sum(time_list)/60,
                 'hr': sum(time_list)/3600
                 })


def get_lanczos_error(outfile: str) -> str:
    return_string = "Lanczos Error not found, job may be running or encountered an error. \n" + \
                    "  see file {}".format(outfile)
    with open(outfile, mode='r') as f:
        for line in f:
            if "Max Lanczos" in line:
                return_string = "{}".format(line.split()[3])
    return return_string
