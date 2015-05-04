__author__ = 'Corey Petty'


def whichswitch(option, writefile, filename):
    """

    :param option: passed option
    :type option: int
    :param writefile: filename that will be written to
    :param filename: filename to write into writefile
    :type filename: str
    :return: null
    """
    if option == 0:
        return
    else:
        writefile.write(filename)
    return