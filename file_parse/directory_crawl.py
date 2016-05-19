__author__ = 'Corey Petty'
import os
import glob
import unittest


def find_jobs(path):
    """
    print job files in directory tree

    TEST USAGE:
        python -m unittest mglob
    """
    def find_job_paths(root, files, base):
        """
        given a job base filename, list related job files that exist
        """
        JOB_SUFFIXES = ['.sh', '.hin', '.in', '.hout', '.out']
        for suffix in JOB_SUFFIXES:
            newfile = base + suffix
            if newfile in files:
                yield os.path.join(root, newfile)
            else:
                yield None

    for root, dirs, files in os.walk(path):
        # process each file base name once
        bases = set(os.path.splitext(file_)[0]
                    for file_ in files)
        for base in bases:
            job_paths = list(find_job_paths(root, files, base))
            if any(job_paths):
                yield job_paths


class TestFind(unittest.TestCase):
    def test_simple(self):
        result = list(find_jobs('temp'))
        self.assertEquals(
            result, [
                [None, None, 'temp/run2.in', None, 'temp/run2.out'],
                ['temp/run.sh', 'temp/run.hin', None, 'temp/run.hout', None],
            ],
            result)
