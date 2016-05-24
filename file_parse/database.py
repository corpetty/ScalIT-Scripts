__author__ = 'Corey Petty'
import pandas as pd
from file_parse.get_parameters import combined_dict_from_inputs
from file_parse.out_info import get_eigenvalues


def print_table(hinfilename, infilename, outfilename) -> pd.DataFrame:
    # get isotope
    isotope = input("Please input the isotopologue of input files: ")

    # get run parameters from input files
    param_dict = combined_dict_from_inputs(hinfilename, infilename)

    # Get states from *.out
    eig_list = get_eigenvalues(outfilename)

    # Get permuatation symmetry
    permutation = ()

    # Create state index

    # Submit entry of states
    dummy = []

    # Format into table
    #  "isotope, Permutation, J_total, j_max, Num_lr, Num_br, Num_theta, Parity, State_index, Energy "
    for num, state in enumerate(eig_list, 1):
        dummy.append([isotope, param_dict["J_total"], param_dict["j_max"],
                      param_dict["num_lr"], param_dict["num_br"],
                      param_dict["num_gm"], param_dict["parity"],
                      param_dict["pist_e0"], num, state])

    df = pd.DataFrame(dummy, columns=["isotope", 'J Total', 'j max',
                                      'num lr', 'num br', 'num gm',
                                      'parity', 'central energy', 'state index', 'state'])

    return df


def make_dataframe(root_dir) -> pd.DataFrame:
    from file_parse.directory_crawl import find_jobs

    # Create columns for DataFrame
    columns = [
        'name',
        'mass_option',
        'permutation',
        'parity',
        'j_total',
        'j_max',
        'num_lr',
        'num_br',
        'num_gm',
        'central_energy',
        'platform',
        'num_cores_hout',
        'num_cores_out',
        'hout_mpi_time',
        'hout_cpu_time',
        'core_hours_hout',
        'num_states_calculated',
        'lanczos_err',
        'out_diag_time',
        'out_lanc_time',
        'out_tot_time',
        'core_hours_out',
        'states',
    ]
    # create dataframe from dictionary
    df = pd.DataFrame(columns=columns)

    jobs = list(find_jobs(root_dir))
    job_dicts = []
    for job in jobs:
        job_dicts.append(make_db_row(job))
    for num, job_dict in enumerate(job_dicts):
        if job_dict is not None:
            df.loc[num] = pd.Series(job_dict)

    return df


def make_db_row(job) -> dict:
    from file_parse.out_info import get_lanczos_error, total_runtime_out, get_eigenvalues, get_central_energy
    from file_parse.script_info import get_num_cores_out, get_permutation, get_platform
    import file_parse.hout_info as hout_info
    #  Check to make sure all files are present
    if not all(job):
        return
    #  Unpack input
    shfile, hinfile, infile, houtfile, outfile = job
    #  initialize empty return dict
    job_dict = {}
    #  Parse files for required parameters and stats
    name, mass_option, j_total, permutation = hout_info.break_apart_path(houtfilename=houtfile)
    num_lr, num_br, num_jmax, num_gm = hout_info.get_basis_size(houtfilename=houtfile)
    mpi_time, cpu_time = hout_info.get_total_runtime(houtfile=houtfile)
    load_time, diag_time, osbw_time, lanc_time = total_runtime_out(outfile=outfile)
    #  Populate return dict
    job_dict['name'] = name
    job_dict['mass_option'] = mass_option
    job_dict['permutation'] = permutation
    job_dict['parity'] = hout_info.get_parity(houtfilename=houtfile)
    job_dict['j_total'] = j_total
    job_dict['j_max'] = num_jmax
    job_dict['num_lr'] = num_lr
    job_dict['num_br'] = num_br
    job_dict['num_gm'] = num_gm
    job_dict['central_energy'] = get_central_energy(outfilename=outfile)
    job_dict['platform'] = get_platform(scriptfilename=shfile)
    job_dict['num_cores_hout'] = hout_info.get_num_cores(houtfilename=houtfile)
    job_dict['num_cores_out'] = get_num_cores_out(scriptfilename=shfile)
    job_dict['hout_mpi_time'] = mpi_time
    job_dict['hout_cpu_time'] = cpu_time
    job_dict['core_hours_hout'] = mpi_time / 3600 * job_dict['num_cores_hout']
    job_dict['num_states_calculated'] = len(get_eigenvalues(outfile=outfile))
    job_dict['lanczos_err'] = get_lanczos_error(outfile=outfile)
    job_dict['out_diag_time'] = diag_time
    job_dict['out_lanc_time'] = lanc_time
    job_dict['out_tot_time'] = load_time + diag_time + osbw_time + lanc_time
    job_dict['core_hours_out'] = float(job_dict['out_tot_time'].seconds) / float(3600) * float(job_dict['num_cores_out'])
    job_dict['states'] = get_eigenvalues(outfile=outfile)
    return job_dict


def plot_df(df):
    import matplotlib.pyplot as plt
    import numpy as np
    print("Start basis: {},{},{}".format(df.num_lr.iloc[0], df.num_br.iloc[0], df.num_gm.iloc[0]))
    num_plots = len(df) - 1
    f, ax = plt.subplots(num_plots, sharex=True, sharey=True, figsize=(12, num_plots * 3))
    for pos in range(num_plots):
        ax[pos].plot(np.array(df.states.iloc[pos + 1]) - np.array(df.states.iloc[pos]))
        ax[pos].set_title('{},{},{}'.format(df.num_lr.iloc[pos + 1], df.num_br.iloc[pos + 1], df.num_gm.iloc[pos + 1]))
