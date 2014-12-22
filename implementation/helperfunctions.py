#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Useful functions"""

def removenekudot(listorstring):
    """Remove all the nekudot from a string, or all the strings in a list.
       It can be nested to any level.
       The original string or list is not changed."""
    nekudot = u"אְאֱאֲאֳאִֵאֶַאָשׂשׁאֹאּאֻ".replace(u"א", "").replace(u"ש", "")
    try:
        for nikud in nekudot:
            listorstring = listorstring.replace(nikud, "")
        return listorstring
    except AttributeError:
        return [removenekudot(newlistorstring) for newlistorstring in listorstring]
