#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pastePoint_cmd.py
A command to paste clipboard content at a picked point in Rhino, bypassing the default behavior of pasting to original coordinates.
Assign to use with the Ctrl+Shift+V.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
February 2025 in Basel, GPL3.0
"""
import rhinoscriptsyntax as rs
import System.Windows.Forms as wf
import Rhino
import scriptcontext as sc

__commandname__ = "pastePoint"

def check_clipboard_formats():
    formats = wf.Clipboard.GetDataObject().GetFormats()
    
    found_image = False
    found_text = False
    for fmt in formats:
        if fmt == "Bitmap" and not found_image:
            print("Clipboard contains an image")
            found_image = True
        
        elif fmt == "Text" and not found_text:
            print("Clipboard contains text")
            found_text = True

def get_object_base_point(obj_id):
        
    if rs.IsBlockInstance(obj_id):
        return rs.BlockInstanceInsertPoint(obj_id)
    
    bbox = rs.BoundingBox(obj_id)
    if not bbox:
        return None
    
    # Calculate the center
    min_pt = bbox[0]
    max_pt = bbox[6]
    center = [(min_pt[0] + max_pt[0])/2, 
              (min_pt[1] + max_pt[1])/2, 
              (min_pt[2] + max_pt[2])/2]
    
    return center

def get_objects_base_point(objects):
    
    if not objects or len(objects) == 0:
        return None
    
    if len(objects) == 1:
        return get_object_base_point(objects[0])
    

    for obj in objects:
        if rs.IsBlockInstance(obj):
            return get_object_base_point(obj)
    
    # If no blocks, calculate the combined bounding box of all objects
    combined_bbox = None
    
    for obj in objects:
        bbox = rs.BoundingBox(obj)
        if not bbox:
            continue
            
        if combined_bbox is None:
            combined_bbox = bbox
        else:
            # Expand combined bbox to include this object's bbox
            for pt in bbox:
                if pt[0] < combined_bbox[0][0]: combined_bbox[0] = (pt[0], combined_bbox[0][1], combined_bbox[0][2])
                if pt[1] < combined_bbox[0][1]: combined_bbox[0] = (combined_bbox[0][0], pt[1], combined_bbox[0][2])
                if pt[2] < combined_bbox[0][2]: combined_bbox[0] = (combined_bbox[0][0], combined_bbox[0][1], pt[2])
                
                if pt[0] > combined_bbox[6][0]: combined_bbox[6] = (pt[0], combined_bbox[6][1], combined_bbox[6][2])
                if pt[1] > combined_bbox[6][1]: combined_bbox[6] = (combined_bbox[6][0], pt[1], combined_bbox[6][2])
                if pt[2] > combined_bbox[6][2]: combined_bbox[6] = (combined_bbox[6][0], combined_bbox[6][1], pt[2])
    
    if not combined_bbox:
        return None
        
    # Calculate center point
    min_pt = combined_bbox[0]
    max_pt = combined_bbox[6]
    center = [(min_pt[0] + max_pt[0])/2, 
              (min_pt[1] + max_pt[1])/2, 
              (min_pt[2] + max_pt[2])/2]
    
    return center

def paste_at_point():
  
    target_point = rs.GetPoint("Pick paste destination point")
    if target_point is None:
        return
   
     
    rs.Command("_Paste", True)
    pasted_objs = rs.LastCreatedObjects()
    
    if not pasted_objs:
        print("No Rhino objects detected in clipboard. Checking other formats...")
        check_clipboard_formats()
        return
    
    try:
        base_point = get_objects_base_point(pasted_objs)
        if not base_point:
            raise ValueError("Could not determine the base point of pasted objects.")
        
   
        translation = rs.VectorCreate(target_point, base_point)
        rs.MoveObjects(pasted_objs, translation)
        print("Objects pasted successfully at the specified point.")
        
    except Exception as e:
        print("An error occurred: " + str(e))
        check_clipboard_formats()
        
def RunCommand(is_interactive):
    paste_at_point()
    return 0
    
if __name__ == "__main__":
    try:
        paste_at_point()
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print("Something went wrong: " + str(e))