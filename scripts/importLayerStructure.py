#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
importLayerStructure.py
Import the layer structure from a selected file to the current Rhino document.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
January 2025 in Basel, GPL3.0
"""


import Rhino
import rhinoscriptsyntax as rs

file = rs.OpenFileName("Select file to import layers from:", extension="3dm")
if file:
    selectedFile = Rhino.FileIO.File3dm.Read(file)

if selectedFile:
    layers = selectedFile.Layers

for layer in layers:
    rs.AddLayer(name=layer.FullPath, color=layer.Color, visible=layer.IsVisible, locked=layer.IsLocked)
