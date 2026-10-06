#! python 2
# -*- coding: utf-8 -*-

"""
objsBlockstoSelectedLayer.py
Moves selected objects and block instances to a chosen layer, including the objects inside the blocks' definitions.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
August 2026 in Basel, GPL3.0
Vibe coded with GPT-5.6 Sol by OpenAI
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

__commandname__ = "MoveBlocksToLayer"

def moveBlocksToLayer():

    # Ask user for target layer
    target_layer = rs.GetLayer("Select target layer")
    if not target_layer:
        print("No layer selected!")
        return

    # Select objects (blocks and/or normal objects)
    objects = rs.GetObjects("Select objects and/or block instances", preselect=True)
    if not objects:
        print("No objects selected!")
        return

    rs.EnableRedraw(False)

    try:
        for i, obj in enumerate(objects):

            if not rs.IsObjectValid(obj):
                continue

            print("Processing object {}/{}".format(i+1, len(objects)))

            # Move the object itself
            rs.ObjectLayer(obj, target_layer)

            # If it is a block instance, move its definition objects too
            if rs.IsBlockInstance(obj):

                block_name = rs.BlockInstanceName(obj)
                definition_objects = rs.BlockObjects(block_name)

                if definition_objects:
                    for def_obj in definition_objects:
                        rs.ObjectLayer(def_obj, target_layer)

        print("Objects and block contents moved successfully!")

    finally:
        rs.EnableRedraw(True)

    return


def RunCommand(is_interactive):
    moveBlocksToLayer()
    return 0


if __name__ == "__main__":
    try:
        moveBlocksToLayer()
    except ValueError as e:
        print(e)
    except Exception:
        print("Something went wrong...")
