#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Compile synonyms.txt"""

from baseclasses import MalbimDataFile
import globalvariables

class Synonyms(MalbimDataFile):
    """Contains lists of synonyms"""
    def __init__(self, synonymsfile):
        self.synonyms = []
        self.oneway = []
        super(Synonyms, self).__init__(synonymsfile)
        self.parse(self.lines)
        self.data = [self.synonyms, self.oneway]

    def parse(self, lines):
        """Parse synonyms.txt into the lists"""
        for line in lines:
            if ">" in line or "<" in line:
                self.parseoneway(line)
            elif "=" in line:
                self.parsesynonym(line)
            else:
                self.raiseerror(line)

    def parsesynonym(self, line):
        """Synonyms are words that are essentially interchangeable
           with regard to what people are likely to search for"""
        addlist = line.split("=")
        if ">" in line or "<" in line or len(addlist) == 1 or "-" in line:
            self.raiseerror(line)

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
            self.raiseerror(line)
        self.oneway += [addlist]

    def raiseerror(self, line):
        msg = ("Each line should have exactly one of '<' or '>',\n"
               "or any number of '=', and no '-'\n"
               "Problematic line:\n" + line)
        super(Synonyms, self).raiseerror(msg)

    def check(self, lines):
        super(Synonyms, self).check(lines, globalvariables.allowedcharacters + "<>")

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
