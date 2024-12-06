#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
objectsByLayer_cmd.py
A command to set the properties of the selected object to "By Layer".
Targeted properties: Object Color, Material, Linetype, Print Color, and Print Width.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
November 2024 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "ObjectsByLayer"

def objectsByLayer():
  
    objects = rs.GetObjects(preselect=True)
    
    if objects:
        for obj in objects:
            if rs.IsObjectValid(obj):
              
                # Set properties to "By Layer"
                rs.ObjectColorSource(obj, 0)
                rs.ObjectMaterialSource(obj, 0)
                rs.ObjectLinetypeSource(obj, 0)
                rs.ObjectPrintColorSource(obj, 0)
                rs.ObjectPrintWidthSource(obj, 0)

    print('Objects properties set byLayer successfully!')
    return 

def RunCommand(is_interactive):

    objectsByLayer()

    return 0


if __name__ == "__main__":
     
    try:
        objectsByLayer()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")
