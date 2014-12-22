#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Main classes for reading from files"""

import globalvariables
from helperfunctions import removenekudot
from baseclasses import ReadFileError, MalbimDataFile

class MalbimIndexFile(MalbimDataFile):
    """Most files should be in this category.  The standard files described
       in README.txt"""
    def __init__(self, datafile, ninitialwords):
        super(MalbimIndexFile, self).__init__(datafile, ninitialwords)
        self.parse(self.lines)

    def parse(self, lines):
        """Assemble it all into a big list"""
        for line in lines:
            unitlist = []
            referencelocation = " ".join(line.split(" ")[:self.ninitialwords])
            for unit in line.split(" ")[self.ninitialwords:]:
                comparedlist = [referencelocation]
                for compared in unit.split("-"):
                    synonymlist = []
                    for synonym in compared.split("="):
                        synonymlist += [synonym]
                        for globalsynonymlist in globalvariables.SYNONYMS.getdata()[0]:
                            if removenekudot(synonym) in removenekudot(globalsynonymlist):
                                synonymlist += globalsynonymlist
                                synonymlist.remove(synonym)
                        for onewaysynonymlist in globalvariables.SYNONYMS.getdata()[1]:
                            if removenekudot(synonym) == removenekudot(onewaysynonymlist[1]):
                                synonymlist += onewaysynonymlist[:1]
                    comparedlist += [synonymlist]
                unitlist += [comparedlist]
            self.data += unitlist

def test():
    """Test this on rishon of Vayeishev"""
    print "Test:"
    myfile = MalbimIndexFile("../Vayeishev/rishon.txt", 2)
    for c in myfile.getdata():
        print c[0] + ":"
        print "\n".join(" ".join(a for a in b) for b in c[1:])
        print

if __name__ == '__main__':
    test()

