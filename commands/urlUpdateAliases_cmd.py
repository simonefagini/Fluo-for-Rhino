#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
urlUpdateAliases_cmd.py
A quick way to offload and then re-import all Rhino aliases from the latest version of rhinoAliases.txt.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
December 2024 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import os
import urllib2

__commandname__ = "UrlUpdateAliases"


def UrlUpdateAliases():
      
    file = urllib2.urlopen("https://raw.githubusercontent.com/simonefagini/Fluo-for-Rhino/refs/heads/main/aliases/rhinoAliases.txt")
    content = [line.decode('utf-8') for line in file.readlines()]

    if not content:
        raise ValueError ("Couldn't load or locate Alias.txt file.")

    # Parse file an "unpacks" aliases and commands
    unchecked_aliases = [line.split( )[0] for line in content]
    aliases = [al.lower() for al in unchecked_aliases]
    fragments = [line.split( )[1:] for line in content]
    commands = [" ".join(fragments[i]) for i in range(0,len(fragments))]

    # Deletes old Rhino aliases
    oldAliasesCount = rs.AliasCount()
    oldAliases = rs.AliasNames()

    for name in oldAliases:
        rs.DeleteAlias(name)

    # Add aliases from txt file
    for i in range (0, len(aliases)):
       rs.AddAlias(aliases[i],commands[i])
      
    return

def RunCommand( is_interactive ):
  
    UrlUpdateAliases()
  
    return 0
    
if __name__ == "__main__":
     
    try:
        UrlUpdateAliases()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")
