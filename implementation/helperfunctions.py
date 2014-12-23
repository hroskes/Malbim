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
    badcharacters = u"\ufeff"
    return removecharacters(listorstring, badcharacters)
