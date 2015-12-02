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
