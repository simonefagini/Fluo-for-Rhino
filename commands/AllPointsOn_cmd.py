#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AllPointsOn_cmd.py
A custom Rhino command to merge the functionality of 'PointsOn and 'SolidPtOn.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
Dec 2024 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "AllPointsOn"


def PointsOn():
    
    filter = rs.filter.curve | rs.filter.surface | rs.filter.polysurface
    selection = rs.GetObjects("Select ojects for control points display:", filter, preselect=True)

    if not selection:
        raise ValueError("No valid objects selected...")
        
    for obj in selection:
        if rs.IsCurve(obj):
            rs.EnableObjectGrips(obj,True)
        else:
            rs.SelectObject(obj)
            rs.Command("_SolidPtOn")
            
    print("Control points are now on!")
    return
    
    
def RunCommand( is_interactive ):
    try:
        PointsOn()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")
    
    return 0
    
    
if __name__ == "__main__":
     
    try:
        PointsOn()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")
