#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Main classes for reading from files"""

import globalvariables
import os
from helperfunctions import removenekudot, removebadcharacters, removeduplicates
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

                if unit.startswith("(") and unit.endswith(")"):
                    comparedlist = ["(" + referencelocation + ")"]
                    unit = unit[1:-1]
                elif unit.startswith("[") and unit.endswith("]"):
                    comparedlist = ["[" + referencelocation + "]"]
                    unit = unit[1:-1]
                else:
                    comparedlist = [referencelocation]

                synonymdata = zip(globalvariables.SYNONYMS.getdata()[0],
                                  removenekudot(globalvariables.SYNONYMS.getdata()[0]))
                onewaydata = zip(globalvariables.SYNONYMS.getdata()[1],
                                  removenekudot(globalvariables.SYNONYMS.getdata()[1]))

                for compared in unit.split("-"):
                    synonymlist = compared.split("=")
                    oldlength = -1
                    while len(synonymlist) > oldlength:
                        oldlength = len(synonymlist)
                        for synonym in synonymlist:
                            wordlist = synonym.split("~")
                            for globalsynonymlist, nonekudot in synonymdata:
                                if removenekudot(synonym) in nonekudot:
                                    synonymlist += globalsynonymlist
                                if len(wordlist) > 1:
                                    for word in wordlist:
                                        if removenekudot(word) in nonekudot:
                                            synonymlist += [synonym.replace(word,globalsynonym) \
                                                                for globalsynonym in globalsynonymlist]
                            for onewaysynonymlist, nonekudot in onewaydata:
                                if removenekudot(synonym) == nonekudot[1]:
                                    synonymlist += onewaysynonymlist[:1]
                            synonymlist = removeduplicates(synonymlist)
                    comparedlist += [synonymlist]
                unitlist += [comparedlist]
            self.data += unitlist

def compileall(directory = ".."):
    data = []
    files = os.listdir(directory)
    for fi in files:
        if fi in globalvariables.specialfiles:
            continue
        elif fi.endswith(".txt"):
            data += MalbimIndexFile(os.path.join(directory, fi), 2).getdata()
        elif os.path.isdir(os.path.join(directory, fi)):
            data += compileall(os.path.join(directory, fi))
    return data

def createdict(data):
    datadict = {}
    for unit in data:
        for compared in unit[1:]:
            for synonym in compared:
                if synonym not in datadict:
                    datadict[synonym] = []
                datadict[synonym] += removebadcharacters([unit])
                datadict[synonym].sort(key = lambda item: item[0])
    return datadict

def test():
    """Test this"""
    print "Test:"
    """
    for c in createdict(compileall())[u"גיד~נשה"]:
        print c[0] + ":"
        print "\n".join(" ".join(a for a in b) for b in c[1:])
        print"""
    keys = createdict(compileall()).keys()
    keys.sort(key = lambda k: removenekudot(k))
    for k in keys:
        print k

if __name__ == '__main__':
    test()

