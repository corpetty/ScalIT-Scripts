__author__ = 'Corey Petty'


def print_run_variables(params: dict, variables: list):
    print("=== Run variables from parameters file ===\n")
    print('J Total:                    {}'.format(variables[0]))
    print('Max little j:               {}'.format(variables[4]))
    print('Little r1 basis functions:  {}'.format(variables[1]))
    print('Little r2 basis functions:  {}'.format(variables[2]))
    print('Big R basis functions:      {}'.format(variables[3]))
    print('Parity:                     {}'.format(params['hin_opts']['parity']))
    print('Permutation:                {}'.format(params['hin_opts']['permutation']))
    print()
