#! python 2
# -*- coding: utf-8 -*-

"""
blocksRenamer.py
Adds a user-defined prefix to the names of all block definitions in the document.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
September 2026 in Basel, GPL3.0
Vibe coded with GPT-5.6 Sol by OpenAI
"""

import rhinoscriptsyntax as rs

def getPrefix():
    prefix = rs.GetString("Insert Prefix")
    
    if prefix is None:
       return
    
    return prefix

def batchRenamer():
    prefix = getPrefix()
    oldBlockNames = rs.BlockNames(True)
        
    if oldBlockNames:
        for name in oldBlockNames:
            newBlockName= (prefix + name)
            rs.RenameBlock (name,newBlockName)
    return

batchRenamer()