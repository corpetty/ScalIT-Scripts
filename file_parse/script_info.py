__author__ = 'Corey Petty'
import re


def get_num_cores_out(scriptfilename: str) -> int:
    """
    Function to parse job script file and retrieve number of cores used in job
    """
    num_cores = 1
    with open(scriptfilename, mode='r') as scriptfile:
        for line in scriptfile:
            if 'PBS -l nodes' in line:
                nodes, cpn = [int(s) for s in re.findall(r'\b\d+\b', line)]
                num_cores = nodes * cpn
                break
            if 'mpirun' in line:
                num_cores = line.split()[2]
    return num_cores


def get_permutation(scriptfilename: str) -> str:
    permutation = ''
    with open(scriptfilename, mode='r') as scriptfile:
        for line in scriptfile:
            for word in line.split():
                if "$BIN_DIR/" in word:
                    permutation = word[-1]
                    break
    return permutation


def get_platform(scriptfilename: str) -> str:
    platform = 'local'
    with open(scriptfilename, mode='r') as scriptfile:
        for line in scriptfile:
            if '#SBATCH' in line:
                platform = 'lonestar'
                break
            elif '#PBS' in line:
                platform = 'eter'
                break
            elif '#$ -q normal.q' in line:
                platform = 'robinson'
                break
            elif '#$ -P hrothgar' in line:
                platform = 'hrothgar'
                break
    return platform
