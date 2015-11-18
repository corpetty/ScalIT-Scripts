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


def eigenvalues(outfile: str) -> list:
    eig_list = []
    with open(outfile, mode='r') as f:
        for num, line in enumerate(f,1):
            if "Max Lanczos" in line:
                break
        for line in f:
            if "---" in line:
                break
            for eig in line.split():
                eig_list.append(float(eig))
    print("The eigenvalues are:")
    for eig in eig_list:
        print('\t{:E}'.format(eig))
    return eig_list
