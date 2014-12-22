"""Base classes for others to inherit from"""

import codecs

class ReadFileError(Exception):
    """General error for reading files"""
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self._msg = msg

    def __str__(self):
        return self._msg


class MalbimDataFile(object):
    """Parent class for data files"""
    def __init__(self, datafile, ninitialwords):
        self.data = []
        self.ninitialwords = ninitialwords
        with codecs.open(datafile, encoding='utf-8') as dataf:
            self.lines = [line.replace("\n", "").replace("\r","") for line in dataf.readlines()]

    def parse(self, lines):
        """Different for different kinds of files"""
        raise NotImplementedError

    def getdata(self):
        """return the data"""
        return self.data

