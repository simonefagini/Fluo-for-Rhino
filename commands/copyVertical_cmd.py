#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
moveVertical_cmd.py
A command to improve the Copy Vertical workflow by preventing Project snap interference when executing the command.
The intended workflow starts with a selected object.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "CopyVertical"


def copyVertical():

    projectOnOff = rs.ProjectOsnaps()

    if projectOnOff:
		rs.ProjectOsnaps(False)
		rs.Command("'_Copy _Vertical")
    else:
		rs.Command("'_Copy _Vertical")

    return


def RunCommand( is_interactive ):
  
  copyVertical()
  
  return 0
    
if __name__ == "__main__":
     
    try:
        copyVertical()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")