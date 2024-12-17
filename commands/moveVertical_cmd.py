#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
moveVertical_cmd.py
A command to improve the Move Vertical workflow by preventing Project snap interference when executing the command.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
December 2024 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "MoveVertical"


def moveVertical():

    projectOnOff = rs.ProjectOsnaps()

    if projectOnOff:
		rs.ProjectOsnaps(False)
		rs.Command(" '_Move _Vertical")
    else:
		rs.Command(" '_Move _Vertical")

    return


def RunCommand( is_interactive ):
  
  moveVertical()
  
  return 0
    
if __name__ == "__main__":
     
    try:
        moveVertical()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")