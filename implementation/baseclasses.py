#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Base classes for others to inherit from"""

import codecs
import re
from helperfunctions import removebadcharacters
import globalvariables

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
        self.check(self.lines)

    def getdata(self):
        """return the data"""
        return self.data

    def raiseerror(self, msg):
        raise ReadFileError(msg = ("Error reading file " + self.datafile + ":\n" + msg))

    def check(self, lines, allowedcharacters = globalvariables.allowedcharacters):
        for line in lines:
            for character in line:
                if character not in allowedcharacters:
                    self.raiseerror("Bad character '" + character + "' in line:\n" + line
                                     + "\nThe allowed characters are:\n" + allowedcharacters)
            for unit in line.split(" "):
                if unit.startswith("@"):
                    unit = unit[1:]
                if "@" in unit:
                    self.raiseerror("@ must come at the beginning of a unit.  Problematic unit:\n" + unit)
                if unit.startswith("(") and unit.endswith(")") \
                     or unit.startswith("[") and unit.endswith("]") \
                     or unit.startswith("{") and unit.endswith("}"):
                    unit = unit[1:-1]
                for char in "()[]{}":
                    if char in unit:
                        self.raiseerror("Brackets and parentheses can only be used around an entire unit.  Problematic unit:\n" + unit)
