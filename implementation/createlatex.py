# -*- coding: UTF-8 -*-

from helperfunctions import *
from malbimdatafile import createdict, compileall
from globalvariables import latexheader
from baseclasses import ReadFileError
import codecs

def createlatex(datadict=None, outputfile="latexoutput.tex"):
    if datadict is None:
        datadict = createdict(compileall())

    latexstring = latexheader

    strings = ["\\section{Words}", "\\section{Grammar}", "\\section{Concepts}", "\\section{Halacha}"]
    for i in range(len(strings)):
        strings[i] = "\\selectlanguage{english}\n" + strings[i] + "\n\\selectlanguage{hebrew}\n\\begin{multicols}{3}\n\\begin{description}\n"
    keys = datadict.keys()
    keys.sort(key = lambda k: removenekudot(k))

    beginstring = "\\item[%s] \\hfill\n"
    beginstring += "\\begin{description}\n"

    endstring = "\\end{description}\n\n"

    for key in keys:
        used = [False, False, False, False]
        for reference in datadict[key]:
            itemstring = (reference[0].replace("(", "").replace(")", "")
                                      .replace("[", "").replace("]", "")
                                      .replace("{", "").replace("}", "")
                                      .replace("-", "--"))
            if "?" in itemstring:
                itemstring = itemstring.replace("?", "") + u' {\\tiny )צ"ע(}'
            if "@" in itemstring:
                itemstring = r"\emph{" + itemstring.replace("@", "") + "}"

            itemstring = "\\item[" + itemstring + "] \\hfill \\\\ \n"
            itemstring += "\\\\ \n".join(", ".join(removeprefixes(b) for b in a if not b.startswith("*")) for a in reference[1:])
            itemstring += "\n"

            if reference[0].startswith("("):
                whichstring = 1
            elif reference[0].startswith("["):
                whichstring = 2
            elif reference[0].startswith("{"):
                whichstring = 3
            else:
                whichstring = 0

            if not used[whichstring]:
                strings[whichstring] += beginstring % key
                used[whichstring] = True
            strings[whichstring] += itemstring

        for i in range(len(strings)):
            if used[i]:
                strings[i] += endstring

    for i in range(len(strings)):
        strings[i] += "\\end{description}\n\\end{multicols}\n\n\n"

    latexstring += strings[0] + strings[1] + strings[2] + strings[3] + "\\end{document}\n"

    latexstring = removenekudot(latexstring)   #Otherwise LaTeX won't compile
                                               #FIX THIS

    with codecs.open(outputfile, mode='w', encoding='utf-8') as f:
        f.write(latexstring)

if __name__ == '__main__':
    try:
        createlatex()
    except ReadFileError as e:
        print unicode(e)
        exit(1)

