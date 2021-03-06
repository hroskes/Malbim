#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Main classes for reading from files"""

import globalvariables
import compilesynonyms
import os
from helperfunctions import *
from baseclasses import MalbimDataFile

class MalbimIndexFile(MalbimDataFile):
    """Most files should be in this category.  The standard files described
       in README.txt"""
    def __init__(self, datafile, infofile):
        self.ninitialwords = infofile.ninitialwords
        self.reference = infofile.reference
        super(MalbimIndexFile, self).__init__(datafile)
        self.parse(self.lines)

    def check(self, lines):
        super(MalbimIndexFile, self).check([" ".join(line.split(" ")[self.ninitialwords:]) for line in lines])
        super(MalbimIndexFile, self).check([" ".join(line.split(" ")[:self.ninitialwords]) for line in lines], globalvariables.allowedcharacters + ",")

    def parse(self, lines):
        """Assemble it all into a big list"""
        if globalvariables.synonyms is None:
            globalvariables.synonyms = compilesynonyms.Synonyms(globalvariables.synonymsfile)
        for line in lines:
            unitlist = []
            repmap = {}
            for referenceword, i in zip(line.split(" ")[:self.ninitialwords], range(self.ninitialwords)):
                repmap["s" + str(i+1)] = referenceword
            try:
                reference = self.reference % repmap
            except KeyError:
                self.raiseerror("This line does not have enough words:\n" + line)
            for unit in line.split(" ")[self.ninitialwords:]:

                if not unit:
                    continue

                thisreference = reference

                unit = unit.replace("?@", "@?")

                if unit.startswith("@"):
                    thisreference = "@" + thisreference
                    unit = unit[1:]
                if unit.startswith("?"):
                    thisreference = "?" + thisreference
                    unit = unit[1:]

                if unit.startswith("(") and unit.endswith(")"):
                    comparedlist = ["(" + thisreference + ")"]
                    unit = unit[1:-1]
                elif unit.startswith("[") and unit.endswith("]"):
                    comparedlist = ["[" + thisreference + "]"]
                    unit = unit[1:-1]
                elif unit.startswith("{") and unit.endswith("}"):
                    comparedlist = ["{" + thisreference + "}"]
                    unit = unit[1:-1]
                else:
                    comparedlist = [thisreference]

                synonymdata = zip(globalvariables.synonyms.getdata()[0],
                                  removenekudot(globalvariables.synonyms.getdata()[0]))
                onewaydata = zip(globalvariables.synonyms.getdata()[1],
                                  removenekudot(globalvariables.synonyms.getdata()[1]))

                for compared in unit.split("-"):
                    synonymlist = compared.split("=")
                    for i in range(len(synonymlist)):
                        if "/" in synonymlist[i]:
                            synonymlist[i] = "*" + synonymlist[i].split("/",1)[0] + "=%" + synonymlist[i].split("/",1)[1]
                        if "/" in synonymlist[i]:
                            self.raiseerror("A word can only have one slash\n" + line)
                    synonymlist = "=".join(synonymlist).split("=")

                    oldlength = -1
                    while len(synonymlist) > oldlength:
                        oldlength = len(synonymlist)
                        for synonym in synonymlist:
                            if synonym.startswith("%") or synonym.startswith("!"):
                                continue
                            wordlist = synonym.split("~")
                            for globalsynonymlist, nonekudot in synonymdata:
                                if lettersonly(synonym) in nonekudot:
                                    synonymlist += ["*" + word for word in globalsynonymlist \
                                                        if word not in synonymlist]
                                if len(wordlist) > 1:
                                    for word in wordlist:
                                        if lettersonly(word) in nonekudot:
                                            synonymlist += ["*" + synonym.replace(word,globalsynonym) \
                                                            for globalsynonym in globalsynonymlist \
                                                            if lettersonly(synonym.replace(word,globalsynonym)) \
                                                               not in lettersonly(synonymlist)]
                            for onewaysynonymlist, nonekudot in onewaydata:
                                if lettersonly(synonym) == nonekudot[1] \
                                and nonekudot[0] not in lettersonly(synonymlist):
                                    synonymlist.append("*" + onewaysynonymlist[0])
                            synonymlist = removeduplicates(synonymlist)
                    comparedlist += [synonymlist]
                comparedlist = removeduplicates(comparedlist)
                unitlist += [comparedlist]
            self.data += unitlist

class InfoFile(MalbimDataFile):
    def __init__(self, datafile):
        super(InfoFile, self).__init__(datafile)
        self.parse(self.lines)

    def parse(self, lines):
        if len(lines) != 2:
            self.raiseerror("info.txt files need to have exactly 2 nonempty, non-comment lines")
        try:
            self.ninitialwords = int(self.lines[0])
        except ValueError:
            self.raiseerror("The first line of info.txt needs to be an integer")

        for i in range(self.ninitialwords):
            self.lines[1] = self.lines[1].replace('\\' + str(i+1), "%(s" + str(i+1) + ")s")

        self.reference = self.lines[1]

    def check(self, lines):
        super(InfoFile, self).check(lines, globalvariables.allowedcharacters + "\\1234567890,")

def compileall(directory = "..", infofile = None):
    data = []
    files = os.listdir(directory)
    for fi in files:
        if fi.endswith("info.txt"):
            infofile = InfoFile(os.path.join(directory,fi))

    for fi in files:
        print fi
        if fi in globalvariables.specialfiles or os.path.islink(fi):
            continue
        elif fi.endswith(".txt"):
            data += MalbimIndexFile(os.path.join(directory, fi), infofile).getdata()
        elif os.path.isdir(os.path.join(directory, fi)):
            data += compileall(directory = os.path.join(directory, fi), infofile = infofile)
    return data

def createdict(data):
    datadict = {}
    for unit in data:
        for compared in unit[1:]:
            for synonym in compared:
                if synonym.startswith("!") or synonym.startswith("%"):
                    continue
                synonym = synonym.replace("*","")
                if synonym not in datadict:
                    datadict[synonym] = []
                datadict[synonym] += removebadcharacters(cleanup([unit],"!*"))
                datadict[synonym].sort(key = lambda item: tosort(item[0]))
    return datadict

def test():
    """Test this"""
    print "Test:"
    keys = createdict(compileall()).keys()
    keys.sort(key = lambda k: removenekudot(k))
    for k in keys:
        print k

if __name__ == '__main__':
    test()

