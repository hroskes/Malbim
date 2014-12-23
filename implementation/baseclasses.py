"""Base classes for others to inherit from"""

import codecs
from helperfunctions import removebadcharacters

class ReadFileError(Exception):
    """General error for reading files"""
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self._msg = msg
        return

    def __str__(self):
        return self._msg


class MalbimDataFile(object):
    """Parent class for data files"""
    def __init__(self, datafile):
        self.datafile = datafile
        self.data = []
        with codecs.open(datafile, encoding='utf-8') as dataf:
            self.lines = [line for line in removebadcharacters(dataf.readlines())\
                               if not line.startswith("#")
                               if not line.replace(" ","") == ""]

    def getdata(self):
        """return the data"""
        return self.data

    def raiseerror(self, msg):
        raise ReadFileError(msg = ("Error reading file " + self.datafile + ":\n" + msg))
