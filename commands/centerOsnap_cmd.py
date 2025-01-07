#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
centerOsnap_cmd.py
A command to toggle the Center object snap on and off in Rhino.
This provides a quick way to enable or disable snapping to the center of circles and arcs during modeling.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
Jan 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc

__commandname__ = "centerOsnap"


def centerOsnap():
    
    centerValue = 32
    actualOsnaps = rs.OsnapMode()
    centerOn = actualOsnaps & centerValue

    if centerOn:
        newOsnaps = actualOsnaps & ~centerValue
    else:
        newOsnaps = actualOsnaps | centerValue
        
    rs.OsnapMode(newOsnaps)
    return

def RunCommand( is_interactive ):
  
  centerOsnap()

  return 0
    
if __name__ == "__main__":
     
    try:
        centerOsnap()
    except ValueError as e:
        print(e)
    except Exception:
        print("Something went wrong...")