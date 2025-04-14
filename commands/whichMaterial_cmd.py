#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
whichMaterial_cmd.py
A command to check which material is applied to a selected object, or to the objects within a selected block,
and return the material name for quick and easy identification.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs


__commandname__ = "whichMaterial"

def get_block_brep_materials(block_instance):
   materials = set()
   
   block_name = rs.BlockInstanceName(block_instance)
   block_objects = rs.BlockObjects(block_name)
   
   if block_objects:
       for obj in block_objects:
           if rs.IsBrep(obj):
               layer = rs.ObjectLayer(obj)
               layer_id = rs.LayerId(layer)
               material_index = rs.LayerMaterialIndex(layer_id)
               material_name = rs.MaterialName(material_index)
               if material_name:
                   materials.add(material_name)
           elif rs.IsBlockInstance(obj):
               # nested blocks
               nested_materials = get_block_brep_materials(obj)
               materials.update(nested_materials)
   
   return materials

def returnMaterial():
    # Select objects
    ids = rs.GetObjects("Select object to return material name.", preselect=True, select=True)
    if not ids:
       print("No objects were selected!")
       return
       
    if len(ids) > 1:
       rs.UnselectAllObjects()
       print("Please select only one object!")
       return
    
    if rs.IsBlockInstance(ids[0]):
       material_names = get_block_brep_materials(ids[0])
       if material_names:
           user_input = rs.ListBox(list(material_names), "Choose a material to copy to clipboard", "Materials")
           if user_input is not None:
               cleaned_input = user_input.replace("/", "")
               rs.ClipboardText(cleaned_input)
    else:
       refLayer = (rs.ObjectLayer(ids[0]))
       layer = rs.LayerId(refLayer)
       material_index = rs.LayerMaterialIndex(layer)
       material_name = rs.MaterialName(material_index)
       user_input = rs.ListBox([material_name], "Choose a material to copy to clipboard", "Materials")
       if user_input is not None:
           cleaned_input = user_input.replace("/", "")
           rs.ClipboardText(cleaned_input)
       print("Material name copied to clipboard")

def template():
      
      returnMaterial()
      
      return

def RunCommand( is_interactive ):
  
  returnMaterial()
  return 0
    
if __name__ == "__main__":
     
    try:
        returnMaterial()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")