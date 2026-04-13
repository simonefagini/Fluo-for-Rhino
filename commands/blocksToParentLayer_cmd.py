#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
blocksToParentLayer_cmd.py
A command to recursively move objects inside selected block instances
to the layer of their parent block instance.
Nested block instances pass their own instance layer to their contents.
This command edits block definitions, so all instances of the same definition
in the document may be affected.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
Vibe coded with ChatGPT
February 2026 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "blocksToParentLayer"


def move_object_to_layer(rh_obj, layer_index):
    attr = rh_obj.Attributes
    attr.LayerIndex = layer_index
    rh_obj.CommitChanges()


def process_instance_definition(idef, target_layer_index, stack=None):
    """
    Recursively process a block definition.

    Direct geometry inside this definition is moved to target_layer_index.
    Nested block contents are processed using the nested instance's own layer.
    stack is used as a guard against circular references.
    """
    if idef is None:
        return

    if stack is None:
        stack = set()

    if idef.Id in stack:
        return

    stack.add(idef.Id)

    try:
        for obj in idef.GetObjects():
            if obj is None:
                continue

            if isinstance(obj, Rhino.DocObjects.InstanceObject):
                nested_idef = obj.InstanceDefinition
                if nested_idef is None:
                    continue

                nested_layer_index = obj.Attributes.LayerIndex
                process_instance_definition(nested_idef, nested_layer_index, stack)

            else:
                move_object_to_layer(obj, target_layer_index)

    finally:
        stack.remove(idef.Id)


def blocksToParentLayer():
    object_ids = rs.GetObjects(
        "Select objects and block instances",
        preselect=True,
        select=True
    )
    if not object_ids:
        return

    doc = Rhino.RhinoDoc.ActiveDoc
    total = len(object_ids)

    for i, obj_id in enumerate(object_ids, 1):
        print("Object {}/{}".format(i, total))

        rh_obj = doc.Objects.Find(obj_id)
        if rh_obj is None:
            continue

        if isinstance(rh_obj, Rhino.DocObjects.InstanceObject):
            idef = rh_obj.InstanceDefinition
            if idef is None:
                continue

            parent_layer_index = rh_obj.Attributes.LayerIndex
            process_instance_definition(idef, parent_layer_index)

        else:
            pass

    doc.Views.Redraw()
    print("Done.")


def RunCommand(is_interactive):
    blocksToParentLayer()
    return 0


if __name__ == "__main__":
    try:
        blocksToParentLayer()
    except Exception as e:
        print(e)