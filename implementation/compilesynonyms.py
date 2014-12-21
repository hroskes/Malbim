#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Compile synonyms.txt"""

import codecs

class ReadFileError(Exception):
    """General error for reading files"""
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self._msg = msg

    def __str__(self):
        return self._msg

class ReadSynonymsError(ReadFileError):
    """Error for reading synonyms.txt"""
    def __init__(self, line):
        self._msg = ("Error reading synonyms.txt.\n"
                     "Each line should have exactly one of '<' or '>',\n"
                     "or any number of '=', and no '-'\n"
                     "Problematic line:\n" + line)
        ReadFileError.__init__(self, self._msg)

    def __str__(self):
        return self._msg

class Synonyms(object):
    """Contains lists of synonyms"""
    def __init__(self, synonymsfile):
        self.synonyms = []
        self.oneway = []
        with codecs.open(synonymsfile, encoding='utf-8') as synonymsf:
            lines = [line.replace("\n", "") for line in synonymsf.readlines()]
        self.parse(lines)


    def parse(self, lines):
        """Parse synonyms.txt into the lists"""
        for line in lines:
            if ">" in line or "<" in line:
                self.parseoneway(line)
            elif "=" in line:
                self.parsesynonym(line)
            else:
                raise ReadSynonymsError(line)

    def parsesynonym(self, line):
        """Synonyms are words that are essentially interchangeable
           with regard to what people are likely to search for"""
        addlist = line.split("=")
        if ">" in line or "<" in line or len(addlist) == 1 or "-" in line:
            raise ReadSynonymsError(line)

        self.synonyms += [addlist]

    def parseoneway(self, line):
        """See README.txt.  One way synonyms are like ספר>ספירה
           and ספר>ספור.  Someone searching for ספר might mean either"""
        addlist = None
        if ">" in line:
            addlist = line.split(">")
        elif "<" in line:
            addlist = line.split("<")
            addlist.reverse()

        if addlist is None or len(addlist) != 2 or "=" in line or "-" in line:
            raise ReadSynonymsError(line)
        self.oneway += [addlist]

def test():
    """Test this on synonyms.txt"""
    print "Test:"
    synonyms = Synonyms("../synonyms.txt")
    print "Synonyms:"
    print "\n".join(" ".join(a) for a in synonyms.synonyms)
    print "\nOne-way synonyms:"
    print "\n".join(" ".join(a) for a in synonyms.oneway)

if __name__ == '__main__':
    test()
