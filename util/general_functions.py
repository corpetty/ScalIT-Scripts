__author__ = 'Corey Petty'

import sys


def dictdump(obj, nested_level=0, output=sys.stdout):  # Currently not used for anything
    """
    Method for print out all the elements of a dictionary object in Python.
    Taken from MrWonderful on StackOverflow.
    Credit: http://stackoverflow.com/questions/15785719/how-to-print-a-dictionary-line-by-line-in-python
    :param obj:
    :param nested_level:
    :param output:
    :return:
    """
    spacing = '   '
    if type(obj) == dict:
        print('%s{' % (nested_level * spacing), output)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print('%s%s:' % ((nested_level + 1) * spacing, k), output)
                dictdump(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v), output)
        print('%s}' % (nested_level * spacing), output)
    elif type(obj) == list:
        print('%s[' % (nested_level * spacing), output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dictdump(v, nested_level + 1, output)
            else:
                print('%s%s' % ((nested_level + 1) * spacing, v), output)
        print('%s]' % (nested_level * spacing), output)
    else:
        print('%s%s' % (nested_level * spacing, obj), output)


def read_dict_from_file(filename: str) -> dict:
    dict_from_file = dict()
    with open(filename, 'r') as infile:
        for line in infile:
            pairs = [line.strip().split('=')]
            for key, value in pairs:
                dict_from_file[key.strip()] = eval(value)
    infile.close()
    return dict_from_file


def dict_from_file_template(inputfilename: str, templatefilename: str) -> dict:
    import shlex
    out_dict = {}
    with open(inputfilename, mode='r') as hinfile:
        infile_tokens = shlex.split(hinfile)
        with open(templatefilename, mode='r') as templatefile:
            template_tokens = shlex.split(templatefile)
            for hin_token, temp_token in zip(infile_tokens, template_tokens):
                out_dict[temp_token] = hin_token
    return out_dict


def check_csv_duplicates(csvfile: str):
    """
        This was copied from user jamylak on
        http://stackoverflow.com/questions/15741564/removing-duplicate-rows-from-a-csv-file-using-a-python-script
    Args:
        csvfile: filename of csv file to check for duplicates

    Returns:
        nothing
    """
    import fileinput
    seen = set()  # set for fast O(1) amortized lookup
    for line in fileinput.FileInput(csvfile, inplace=1):
        if line in seen:
            continue  # skip duplicate

        seen.add(line)
        print(line,)  # standard output is now redirected to the file
