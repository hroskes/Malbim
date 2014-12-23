from helperfunctions import removenekudot
from malbimdatafile import createdict, compileall
from globalvariables import latexheader
import codecs

def createlatex(datadict=None, outputfile="latexoutput.tex"):
    if datadict is None:
        datadict = createdict(compileall())

    #with codecs.open("latexheader.tex", encoding='utf-8') as f:
    #    latexstring = f.read()
    latexstring = latexheader

    strings = ["\\section{Words}", "\\section{Grammar}", "\\section{Concepts}"]
    for i in range(len(strings)):
        strings[i] = "\\selectlanguage{english}\n" + strings[i] + "\n\\selectlanguage{hebrew}\n\\begin{multicols}{3}\n\\begin{description}\n"
    keys = datadict.keys()
    keys.sort(key = lambda k: removenekudot(k))

    beginstring = "\\item[%s] \\hfill\n"
    beginstring += "\\begin{description}\n"

    endstring = "\\end{description}\n\n"

    for key in keys:
        used = [False, False, False]
        for reference in datadict[key]:
            itemstring = ""
            itemstring += "\\item[" + (reference[0].replace("(", "").replace(")", "")
                                                   .replace("[", "").replace("]", "")
                                                   .replace("-", "--")) + "] \\hfill \\\\ \n"
            itemstring += "\\\\ \n".join(", ".join(b for b in a) for a in reference[1:])
            itemstring += "\n"

            if reference[0].startswith("("):
                whichstring = 1
            elif reference[0].startswith("["):
                whichstring = 2
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

    latexstring += strings[0] + strings[1] + strings[2] + "\\end{document}\n"

    latexstring = removenekudot(latexstring)   #Otherwise LaTeX won't compile
                                               #FIX THIS

    with codecs.open(outputfile, mode='w', encoding='utf-8') as f:
        f.write(latexstring)

if __name__ == '__main__':
    createlatex()

