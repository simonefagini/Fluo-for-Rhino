#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
sortAliases.py
helping tool to sort aliases alphabetically. 
rhino stores aliases in the order they are added but displays them alphabetically.
keeps the rhinoAliases.txt file neatly sorted for version control
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
nov 2024 in basel, GPL3.0
"""

myPath = '../../rhinoAliases.txt' # Local path to file
bacPath = myPath.replace(".txt", "_bac.txt")

file = open(myPath,'r')
content=file.readlines()
file.close()

# Makes a _bac file of the original aliases in the same folder
sorted_file = open(bacPath,'w')
sorted_file.writelines(content)
sorted_file.close()


unchecked_aliases = [line.split( )[0] for line in content]
aliases = [al.lower() for al in unchecked_aliases]	  #lowers capital letters for consistency
fragments = [line.split( )[1:] for line in content]
commands = [" ".join(fragments[i]) for i in range(0,len(fragments))]
sorted_aliases = [f"{alias} {command}" for alias, command in sorted(zip(aliases,commands))]

sorted_file = open(myPath,'w')
sorted_file.writelines('\n'.join(sorted_aliases))
sorted_file.close()
