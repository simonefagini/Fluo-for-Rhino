#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
rotateRandom_cmd.py
A command to randomly rotate selected objects individually around their own center points.
Adds a touch of chaos and variation.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basle, GPL3.0
"""

import rhinoscriptsyntax as rs
import random


__commandname__ = "rotateRandom"

def boxCenter(box):
    
    if not box:
        return None
    
    # Calculate the center
    min_pt = box[0]
    max_pt = box[6]
    center = [(min_pt[0] + max_pt[0])/2, 
              (min_pt[1] + max_pt[1])/2, 
              (min_pt[2] + max_pt[2])/2]
    
    return center

def getRotationAxis():
    worldAxis = ["x","y","z"]
    isXTrue = False
    isYTrue = False
    isZTrue = False

    axis = rs.MultiListBox(worldAxis, "Axis: (multiple choice)")

    for xyz in axis:
        if str(xyz) == "x":
            isXTrue = True
        elif str(xyz) == "y":
            isYTrue = True
        elif str(xyz) == "z":
            isZTrue = True
    return (isXTrue, isYTrue,isZTrue)
    
def getAngles(axis):
    
    if axis is None:  # User canceled
        return None
    
    if axis[0] == True:
        xRot = rs.GetReal("X axis, max rotation:", 0, 0, 360)
        if xRot is None:  # User canceled
            return None
        if xRot < 0 or xRot > 360:
            raise ValueError("Rotation must be between 0 and 360 degrees")
    else:
       xRot = 0
    
    if axis[1] == True:
        yRot = rs.GetReal("Y axis, max rotation:", 0, 0, 360)
        if yRot is None:  # User canceled
            return None
        if yRot < 0 or yRot > 360:
            raise ValueError("Rotation must be between 0 and 360 degrees")
    else:
       yRot = 0
    
    if axis[2] == True:
        zRot = rs.GetReal("Z axis, max rotation:", 0, 0, 360)
        if zRot is None:  # User canceled
            return None
        if zRot < 0 or zRot > 360:
            raise ValueError("Rotation must be between 0 and 360 degrees")
    else:
       zRot = 0
    
    return xRot, yRot, zRot

def rotateRandom():
    centerPoints = []
    rotationAmounts = []
    
    ids = rs.GetObjects("Select objects:", preselect=True, select=True)
    if not ids:
        print("No objects selected.")
        return
        
    random.shuffle(ids)

    for id in ids:
        if not rs.IsBlockInstance(id):
            box = rs.BoundingBox(id)
            if box:
                centerPoints.append(boxCenter(box))
        else:
            centerPoints.append(rs.BlockInstanceInsertPoint(id))
    
    maxRotation = (getAngles(getRotationAxis()))
    
    
    
    for point in centerPoints:
        print("Rotating objects....")
        xRotation = random.uniform(0,maxRotation[0])
        yRotation = random.uniform(0,maxRotation[1])
        zRotation = random.uniform(0,maxRotation[2])
        
        rotationAmounts.append([xRotation,yRotation,zRotation])
    
    
    for index, (id, center, rotation) in enumerate(zip(ids, centerPoints, rotationAmounts)):
        rs.RotateObject(id, center, rotationAmounts[index][0], axis=[1,0,0])  # X-axis rotation
        rs.RotateObject(id, center, rotationAmounts[index][1], axis=[0,1,0])  # Y-axis rotation 
        rs.RotateObject(id, center, rotationAmounts[index][2], axis=[0,0,1])  # Z-axis rotation
    
    print(str(len(ids)) + " objects rotated successfully!")
    
    
    return


def RunCommand( is_interactive ):
    
  
  rotateRandom()

  return 0
    
if __name__ == "__main__":
     
    try:
        rotateRandom()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")