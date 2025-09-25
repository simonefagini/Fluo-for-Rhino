#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dwg_cmd.py
Silently export the document to DWG in the same location.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
September 2025 in Basel, GPL3.0
"""
import rhinoscriptsyntax as rs

__commandname__ = "dwg"

def toDWG():
    DWG_VERSION = "7"
    SAVE_SMALL = "No"
    GEOMETRY_ONLY = "Yes"
    SAVE_TEXTURES = "No"
    SAVE_PLUGIN_DATA = "No"
    
    doc_path = rs.DocumentPath()
    doc_name = rs.DocumentName()
    
    if not doc_path or not doc_name:
        print("Document must be saved first!")
        return
    
    base_name = doc_name[:-4]
    dwg_file = chr(34) + doc_path + base_name + '.dwg' + chr(34)
    print("Exporting to: " + dwg_file)
    
    settings = "_Version=" + DWG_VERSION + " _SaveSmall=" + SAVE_SMALL + " _GeometryOnly=" + GEOMETRY_ONLY + " _SaveTextures=" + SAVE_TEXTURES + " _SavePlugInData=" + SAVE_PLUGIN_DATA
    command = "_NoEcho _-ExportAll " + dwg_file + " " + settings + " _Enter"
    
    rs.Command(command)

def RunCommand(is_interactive):
    toDWG()
    return 0

if __name__ == "__main__":
    try:
        toDWG()
    except ValueError as e:
        print(e)
    except Exception:
        print("Something went wrong...")