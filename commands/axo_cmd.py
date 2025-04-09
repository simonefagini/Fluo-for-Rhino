#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
axo_cmd.py
Python script for Rhino that deforms selected objects into axonometric projections based on customizable rotation angles.
Data is preserved as object attributes for an undestructive workflow,  with full block compatibility.
The 'deaxo' command reverts objects to their original condition.

Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

__commandname__ = "axo"


def isAxo():
    if "isAxo" in sc.sticky:
        isAxo = sc.sticky["isAxo"]
        return(isAxo)
        
    else:
        isAxo = False
        sc.sticky["isAxo"] = isAxo
        return(isAxo)

def tagAxoObjs(objects, center, degs):
    for obj in objects:
        rs.SetUserText(obj, "axoed", "True")
        rs.SetUserText(obj, "axoDeg", degs)
        rs.SetUserText(obj, "axoCenter", center)
    return

def Axo():
    objects = rs.GetObjects(preselect=True)
    if objects == None:
        return
            
    currentCPlane = rs.ViewCPlane(None)
    centerPoint = currentCPlane[0]
    xCenter, yCenter, zCenter = centerPoint
    shearPoint = rs.CreatePoint(xCenter, yCenter, zCenter+100)


    rotationDegs = rs.GetInteger("Enter the rotation amount:", 30)
    shearDegs = -45

    for obj in objects:
        rs.RotateObject(obj, centerPoint, rotationDegs, axis=[0,0,1])
        rs.ViewCPlane(None, rs.WorldYZPlane())
        rs.ShearObject(obj, centerPoint, shearPoint, shearDegs, copy=False)
        rs.ViewCPlane(None, currentCPlane)
        tagAxoObjs(objects, centerPoint, rotationDegs)
        sc.sticky["isAxo"] = True
        
    return
    
def RunCommand( is_interactive ):
  
  Axo()
  
  return 0
    
if __name__ == "__main__":
     
    try:
        Axo()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")