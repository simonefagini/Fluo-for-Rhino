#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
shake_cmd.py
A command to randomly rotate selected objects individually around their own center points.
Adds a touch of chaos and variation.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basle, GPL3.0
"""

import rhinoscriptsyntax as rs
import random


__commandname__ = "shake"

    
def getMaxs():
    
    xMax = rs.GetReal("X, max shaking amplitude", 0)
    if xMax is None:  # User canceled
        return
       
    yMax = rs.GetReal("Y, max shaking amplitude", 0)
    if yMax is None:  # User canceled
        return
       
    zMax = rs.GetReal("Z, max shaking amplitude", 0)
    if zMax is None:  # User canceled
        return

    return xMax, yMax, zMax

def shake():
    counter = 1
    shakingAmplitudes = []
    
    
    ids = rs.GetObjects("Select objects:", preselect=True, select=True)
    if not ids:
        print("No objects selected.")
        return
        
    random.shuffle(ids)
    
    maxAmplitudes = getMaxs()
    print(maxAmplitudes)
    
    
    for id in ids:
        xShake = random.uniform((maxAmplitudes[0])*-1,maxAmplitudes[0])
        yShake = random.uniform((maxAmplitudes[1])*-1,maxAmplitudes[1])
        zShake = random.uniform((maxAmplitudes[2])*-1,maxAmplitudes[2])
        
        shakingAmplitudes.append([xShake,yShake,zShake])
        
    
    for index, (id, rotation) in enumerate(zip(ids, shakingAmplitudes)):
        
        print("Shaking objects....")
        print(str(counter) + " / " + str(len(ids)))
        counter += 1
        rs.MoveObject(id, shakingAmplitudes[index])
        
        #tagging
        rs.SetUserText(id, "shaken", "True")
        rs.SetUserText(id, "translation", shakingAmplitudes[index])
    
    print(str(len(ids)) + " objects were shaken successfully!")
    
    
    return


def RunCommand( is_interactive ):
    
  
  shake()

  return 0
    
if __name__ == "__main__":
     
    try:
        shake()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")