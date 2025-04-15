#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
shake_cmd.py
A command to reset previously shaken objects.
Only restores translation vectors applied with the shake_cmd.py command.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basle, GPL3.0
"""

import rhinoscriptsyntax as rs
import random


__commandname__ = "unshake"


def unshake():
    
    counter = 1
    
    ids = rs.GetObjects("Select objects:", preselect=True, select=True)
    
    if not ids:
        print("No objects selected.")
        return
        
    for id in ids:
        if rs.GetUserText(id, "shaken") == "True":
            prevShake = rs.GetUserText(id, "translation")
            
            prevIntShake = prevShake.split(",")
            
            xUnshake = float(prevIntShake[0][1:])
            yUnshake = float(prevIntShake[1])
            zUnshake = float(prevIntShake[2][:-1])
            
            translationShake = [-xUnshake, -yUnshake, -zUnshake]
        else:
            translationShake = [0,0,0]
            
        print("Restoring objects....")
        print(str(counter) + " / " + str(len(ids)))
        counter += 1
        rs.MoveObject(id, translationShake)
        
        #tagging
        rs.SetUserText(id, "translation", "")
        rs.SetUserText(id, "shaken", "")
        
    print(str(len(ids)) + " objects restored successfully!")
    
    return


def RunCommand( is_interactive ):
    
  
  unshake()

  return 0
    
if __name__ == "__main__":
     
    try:
        unshake()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")