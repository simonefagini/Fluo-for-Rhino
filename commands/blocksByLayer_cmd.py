#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
blocksByLayer_cmd.py
A command to set the properties of the selected objects to "By Layer".
Upgraded from the objectsByLayer_cmd.py to recursively include Blocks.
Targeted properties: Object Color, Material, Linetype, Print Color, and Print Width.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
February 2026 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "blocksByLayer"


def set_object_by_layer(rh_obj):

    attr = rh_obj.Attributes
    attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
    attr.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromLayer
    attr.LinetypeSource = Rhino.DocObjects.ObjectLinetypeSource.LinetypeFromLayer
    attr.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromLayer
    attr.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromLayer
    rh_obj.CommitChanges()


def process_instance_definition(idef, visited):
    
    if idef.Id in visited:
        return
    visited.add(idef.Id)

    for obj in idef.GetObjects():
        if isinstance(obj, Rhino.DocObjects.InstanceObject):
            nested_idef = obj.InstanceDefinition
            if nested_idef:
                process_instance_definition(nested_idef, visited)
        else:
            set_object_by_layer(obj)


def blocksByLayer():
    objects = rs.GetObjects(preselect=True)
    if not objects:
        return

    doc = Rhino.RhinoDoc.ActiveDoc
    visited_defs = set()

    counter = 0
    total = len(objects)

    for obj_id in objects:
        counter += 1
        print("Object {}/{}".format(counter, total))

        rh_obj = doc.Objects.Find(obj_id)
        if not rh_obj:
            continue

        # Block instance
        if isinstance(rh_obj, Rhino.DocObjects.InstanceObject):
            idef = rh_obj.InstanceDefinition
            if idef:
                process_instance_definition(idef, visited_defs)

        # Normal object
        else:
            set_object_by_layer(rh_obj)

    doc.Views.Redraw()


def RunCommand(is_interactive):
    blocksByLayer()
    return 0


if __name__ == "__main__":
    try:
        blocksByLayer()
    except Exception as e:
        print("Something went wrong:", e)
