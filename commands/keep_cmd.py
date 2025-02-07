#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
keep_cmd.py
A command to randomly keep a user-defined percentage of pre-selected objects in Rhino, useful for quick decimation and random sampling.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
February 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import random

__commandname__ = "keep"


def keep():
    # Select objects
    ids = rs.GetObjects("Select objects:",preselect=True, select=True)

    if not ids:
        print("No objects were selected!")
        return


    # Get user input
    percentage = rs.GetInteger("Which percentage do you want to keep?",50,0,100)
    if percentage == None:
        return
    
    objs = random.sample(ids, len(ids) - int(len(ids) * (float(percentage) / 100)))
    rs.UnselectObjects(objs)
      
    return


def RunCommand( is_interactive ):
    
    keep()
    return 0
    
if __name__ == "__main__":
     
    try:
        keep()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")