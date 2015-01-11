#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""For global variables"""

synonyms = None
synonymsfile = "../synonyms.txt"

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

locationlist = [
u"בראשית",
u"שמות",
u"ויקרא",
u"במדבר",
u"דברים",
u"יהושע",
u"שופטים",
u"שמואל",
u"מלכים",
u"ישעיה",
u"ירמיה",
u"יחזקאל",
u"הושע",
u"יואל",
u"עמוס",
u"עובדיה",
u"יונה",
u"מיכה",
u"נחום",
u"חבקוק",
u"צפניה",
u"חגי",
u"זכריה",
u"מלאכי",
u"תהלים",
u"משלי",
u"איוב",
u"שיר השירים",
u"רות",
u"איכה",
u"קהלת",
u"אסתר",
u"דניאל",
u"עזרא",
u"נחמיה",
u"דברי הימים"
]

endprioritysortlist = [
u"שאלות",
None,
u"תורה אור",
u"באור מלים"
]

allowedcharacters = u"אְבֱגֲדֳהִוֵזֶחַטָיֹכּלֻמנסעפצקרשׁׂתךםןףץ~][)({}-='*!%/ "
