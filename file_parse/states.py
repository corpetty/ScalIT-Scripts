__author__ = 'Corey Petty'


def sort_splittings(states: list) -> list:
    """
    Splits up duplicates in Ozone eigenstates for state characterization
    Current threshhold for splitting is set to < 1 cm^-1
    Args:
        states: list of calculated eigenvalues as ScalIT outputs them

    Returns: two column list, where duplicates are next to each other

    """
    eh2cm = 219474.63  # wavenumber conversion
    sorted_list = []
    i = 0
    while i < len(states) - 2:
        if (states[i + 1] - states[i]) * eh2cm < 1.0:  # in wavenumbers
            sorted_list.append([states[i], states[i + 1]])
            i += 1
        else:
            sorted_list.append([states[i]])
        i += 1
    return sorted_list


# TODO: finish this, it is in progress
def state_labels(states: list) -> list:
    eh2cm = 219474.63  # wavenumber conversion
    # Get first Permutation
    # Check if each state is paired or not

