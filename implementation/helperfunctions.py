#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Useful functions"""

def removecharacters(listorstring, characters):
    try:
        for character in characters:
            listorstring = listorstring.replace(character, "")
        return listorstring
    except AttributeError:
        try:
            return {key:removecharacters(listorstring[key], characters) for key in listorstring.keys()}
        except AttributeError:
            return [removecharacters(newlistorstring, characters) for newlistorstring in listorstring]


def removenekudot(listorstring):
    """Remove all the nekudot from a string, or all the strings in a list.
       It can be nested to any level.
       The original string or list is not changed."""
    nekudot = u"אְאֱאֲאֳאִֵאֶַאָשׂשׁאֹאּאֻ".replace(u"א", "").replace(u"ש", "")
    return removecharacters(listorstring, nekudot)

def removebadcharacters(listorstring):
    badcharacters = u"\ufeff\n\r"
    return removecharacters(listorstring, badcharacters)

def removeduplicates(inlist):
    for a in inlist:
        listcopy = inlist[:]
        listcopy.reverse()
        listcopy.remove(a)
        listcopy.reverse()
        if a in listcopy:
            return removeduplicates(listcopy)
    return inlist

def tosort(reference):
    import globalvariables

    for i, location in zip(range(len(globalvariables.locationlist)), globalvariables.locationlist):
        reference = reference.replace(location, str(i))

    for i in [u"תורה אור", u"באור מלים"]:   #no need to distinguish because תורה אור is only in the Torah
        if i in reference:                  #and באור מלים is only in some of Nach.
            reference = reference.replace(i + " ", "") + "1"

    if u"שאלות" in reference:
        reference = reference.replace(u"שאלות ","")
    else:
        reference = reference + "0"

    reference = reference.replace(u"טו", u"יה")
    reference = reference.replace(u"טז", u"יו")

    return reference
