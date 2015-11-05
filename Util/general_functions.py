__author__ = 'Corey Petty'

import sys


def dictdump(obj, nested_level=0, output=sys.stdout):
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
        print >> output, '%s{' % (nested_level * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                dictdump(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
        print >> output, '%s}' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % (nested_level * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                dictdump(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % (nested_level * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)
