#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
objects2sublayers.py
Randomly spreads selected objects into a chosen number of new sublayers, each with its own color.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basel, GPL3.0
"""


import rhinoscriptsyntax as rs
import scriptcontext
import random
from System.Drawing import Color

# Select objects
ids = rs.GetObjects("Select object to distribute randomly on sublayers.",preselect=True, select=True)
random.shuffle(ids)

if not ids:
    print("No objects were selected!")
    exit()
    
# Check wheter valid selection is bigger than one
if len(ids) < 2:
        rs.UnselectAllObjects()
        print("Please select more than one object.")
        exit()
        #RESTART


# Get user variations number
variations = rs.GetInteger("Insert the number of sublayers:",3,1,(len(ids)))
    

subLayerName = rs.GetString("Insert the name of the sublayers:")
if subLayerName == None: 
    subLayerName = "Sublayer"

refLayer = (rs.ObjectLayer(ids[0]))
    

for x in range(variations):
    suffix = str("::" + subLayerName + str(x+1))
    intensity = int(200 - (100 * (x / (variations-1))))
    layColor = Color.FromArgb(255, intensity, 0, 0)
    layName = refLayer + suffix
    rs.AddLayer(name=layName, color=layColor)
    
    
for i, item in enumerate(ids):
    destinationLayer = refLayer + "::" + subLayerName + str((i % variations)+1)
    rs.ObjectLayer(item, destinationLayer)
    
rs.UnselectAllObjects()
