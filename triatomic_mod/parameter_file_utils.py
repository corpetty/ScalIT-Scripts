__author__ = 'Corey Petty'


def print_run_variables(params: dict, variables: list):
    print("=== Run variables from parameters file ===\n")
    print('J Total:                   {}'.format(variables[0]))
    print('Max little j:              {}'.format(variables[3]))
    print('Little r basis functions:  {}'.format(variables[1]))
    print('Big R basis functions:     {}'.format(variables[2]))
    print('Parity:                    {}'.format(params['hin_opts']['parity']))
    print('Permutation:               {}'.format(params['hin_opts']['permutation']))
    print()
