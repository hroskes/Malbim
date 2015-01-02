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

def removeprefixes(listorstring):
    prefixes = "*!%"
    return removecharacters(listorstring, prefixes)

def lettersonly(listorstring):
    nekudotandprefixes = "*!" + u"אְאֱאֲאֳאִֵאֶַאָשׂשׁאֹאּאֻ".replace(u"א", "").replace(u"ש", "")
    return removecharacters(listorstring, nekudotandprefixes)

def removebadcharacters(listorstring):
    badcharacters = u"\ufeff\n\r"
    return removecharacters(listorstring, badcharacters)

def removeduplicates(inlist):
    for a in inlist:
        listcopy = inlist[:]
        listcopy.reverse()
        if removeprefixes(a) in listcopy:
            listcopy.remove(removeprefixes(a))
        elif a.replace("!","*") in listcopy:
            listcopy.remove(a.replace("!","*"))
        elif a.replace("!","%") in listcopy:
            listcopy.remove(a.replace("!","%"))
        else:
            listcopy.remove(a)
        listcopy.reverse()
        if a in listcopy:
            return removeduplicates(listcopy)
    return inlist

def cleanup(inlist, cleanupcharacters):
    outlist = inlist[:]
    for index, a in enumerate(outlist):
        for character in cleanupcharacters:
            try:
                if a.startswith(character):
                    outlist.remove(a)
            except AttributeError:
                outlist[index] = cleanup(a, cleanupcharacters)
    return outlist

def tosort(reference):
    import globalvariables

    for i, location in zip(range(len(globalvariables.locationlist)), globalvariables.locationlist):
        reference = reference.replace(location, str(i))

    addstring = None
    for i, item in zip(range(len(globalvariables.endprioritysortlist)), globalvariables.endprioritysortlist):
        if item is not None and item in reference:
            reference = reference.replace(item + " ", "") + str(i)
            addstring = ""
        elif item is None and addstring is None:
            addstring = str(i)
    reference += addstring

    if u"שאלות" in reference:
        reference = reference.replace(u"שאלות ","")
    else:
        reference = reference + "0"

    reference = reference.replace(u"טו", u"יה")
    reference = reference.replace(u"טז", u"יו")

    return reference
