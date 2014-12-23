"""For global variables"""

import compilesynonyms

SYNONYMS = compilesynonyms.Synonyms("../synonyms.txt")
specialfiles = ["synonyms.txt", "info.txt", "implementation"]

latexheader = r"""\documentclass[11pt]{article}
\usepackage{geometry}
\geometry{verbose,tmargin=1.00in,bmargin=1.00in,lmargin=1.0in,rmargin=1.0in}

\usepackage{multicol}
\setlength{\columnseprule}{0.4pt}
\RLmulticolcolumns

\usepackage[utf8x]{inputenc}
\usepackage[hebrew,english]{babel}
\usepackage{hebcal}
\usepackage[hidelinks]{hyperref}

\begin{document}
\selectlanguage{english}
\title{Malbim index}
\author{Heshy Roskes}
\date{\selectlanguage{english}\today\hfill\selectlanguage{hebrew}\hebrewtoday}

\maketitle
\tableofcontents

"""
