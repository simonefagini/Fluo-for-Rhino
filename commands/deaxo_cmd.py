#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deaxo_cmd.py
Companion command to revert axonometrically projected objects back to their original condition with a single click.
Maintains all object properties while removing projection transformations, keeping your Rhino workflow seamless and non-destructive.
Written to be used in documents where the "axo" command has previously been executed

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

def selAxoed():
    rs.UnselectAllObjects()
    all_objs = rs.AllObjects()
    axoed_objs = []
    counter = 1
    
    for obj in all_objs:
        
        if rs.GetUserText(obj, "axoed") == "True":
            axoed_objs.append(obj)
        print("Objs " + str(counter) + "/" + str(len(all_objs)))
        counter += 1

    if axoed_objs:
        rs.SelectObjects(axoed_objs)
        #print(str(len(axoed_objs)) + " axoed objects selected!")
    return axoed_objs

def removeAxoUserText(obj):
    rs.SetUserText(obj, "axoed", "")
    rs.SetUserText(obj, "axoDeg", "")
    rs.SetUserText(obj, "axoCenter", "")

def deAxo():
    if isAxo() == True:
        objects = selAxoed()
    else:
        print("No axo information found in the current file.")
        print("Please use the command Axo first")
        return
        
    currentCPlane = rs.ViewCPlane(None)
    if objects == None:
        return  # Changed from quit() to return

    for obj in objects:
        # Get the stored center point as a string
        centerPoint_str = rs.GetUserText(obj, "axoCenter")
        centerPoint_parts = centerPoint_str.split(",")
        
        # Convert to floats instead of integers
        xCenter = float(centerPoint_parts[0])
        yCenter = float(centerPoint_parts[1])
        zCenter = float(centerPoint_parts[2])
        
        # Create proper point objects
        centerPoint = rs.CreatePoint(xCenter, yCenter, zCenter)
        shearPoint = rs.CreatePoint(xCenter, yCenter, zCenter+100)
        
        # Get rotation degrees
        rotationDegs = float(rs.GetUserText(obj, "axoDeg")) * -1
        shearDegs = 45  # Removed unnecessary plus sign
        
        rs.ViewCPlane(None, rs.WorldYZPlane())
        rs.ShearObject(obj, centerPoint, shearPoint, shearDegs, copy=False)
        rs.ViewCPlane(None, currentCPlane)
        rs.RotateObject(obj, centerPoint, rotationDegs, axis=[0,0,1])
        
        removeAxoUserText(obj)
        
        if "isAxo" in sc.sticky:
            axo_status = False
            sc.sticky["isAxo"] = axo_status
            
    print("Deaxo complete successfully!")
        
    return
    
    
def RunCommand( is_interactive ):
  
  deAxo()
  
  return 0
    
if __name__ == "__main__":
     
    try:
        deAxo()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")