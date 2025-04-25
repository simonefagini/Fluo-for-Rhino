#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
count_cmd.py
A simple command that counts selected objects.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "count"


def count():
    # Select objects
    ids = rs.GetObjects("Select objects:", preselect=True, select=True)
    
    if not ids:
        print("No objects were selected!")
        return
    
    blocks = 0
    curves = 0
    polysurfaces = 0
    crv = 0
    points = 0
    meshes = 0
    lights = 0
    hatches = 0
    other = 0
    
    for id in ids:
        obj_type = rs.ObjectType(id)
        if obj_type == 4096:            #Block instance
            blocks += 1
        elif obj_type == 4:             #Curve
            curves += 1
        elif obj_type == 16:            #Polysurface
            polysurfaces += 1
        elif obj_type == 8:             #Surface/Crv
            crv += 1
        elif obj_type == 1:             #Point
            points += 1
        elif obj_type == 32:            #Mesh
            meshes += 1
        elif obj_type == 256:           #Light
            lights += 1
        elif obj_type == 512:           #Hatch
            hatches += 1
        else:
            other += 1
    
    
    message = "TOTAL\n"
    message += str(len(ids)) + " objects\n\n"
    message += "TYPE                                                   \n"
    
    
    if blocks > 0:
        message += str(blocks) + " Block Instances\n"
    if crv > 0:
        message += str(crv) + " Crv\n"
    if polysurfaces > 0:
        message += str(polysurfaces) + " Polysurfaces\n"
    if curves > 0:
        message += str(curves) + " Curves\n"
    if points > 0:
        message += str(points) + " Points\n"
    if meshes > 0:
        message += str(meshes) + " Meshes\n"
    if lights > 0:
        message += str(lights) + " Lights\n"
    if hatches > 0:
        message += str(hatches) + " Hatches\n"
    if other > 0:
        message += str(other) + " Other"


    rs.MessageBox(message, 64, "Object Count")
    return


def RunCommand( is_interactive ):
  
  count()
  return 0
    
if __name__ == "__main__":
     
    try:
        count()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")