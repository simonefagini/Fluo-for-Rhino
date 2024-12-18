#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dupAllBorder_cmd.py
A custom Rhino command to merge the functionality of 'DupBorder and 'DupFaceBorder.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
Dec 2024 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc

__commandname__ = "dupAllBorder"


def dupAllBorder():
    
    filter = rs.filter.surface | rs.filter.hatch
    selection = rs.GetObjects("Select face, surface or hatch", filter, preselect=True)
    crvSel = []
    selNone = []

    if not selection:
        raise ValueError("No valid object selected...")
        
    for obj in selection:
        if rs.IsSurface(obj):
            crvFaces = rs.DuplicateSurfaceBorder(obj, type=0)
            crvSel.append(crvFaces)
            rs.UnselectAllObjects()
            
            
        elif rs.IsHatch:
            geom = rs.coercegeometry(obj)
            borders = geom.Get3dCurves(True)
            for border in borders:
                crvSel.append(sc.doc.Objects.AddCurve(border))
        else:
            pass
    
    
    rs.SelectObjects(crvSel)
    if len(crvSel) == 1:
        print("1 border was created..")
    else:
        print(str(len(crvSel)) + " borders were created..")
    return
    
    
def RunCommand( is_interactive ):
    try:
        dupAllBorder()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")
    
    return 0
    
    
if __name__ == "__main__":
     
    try:
        dupAllBorder()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")