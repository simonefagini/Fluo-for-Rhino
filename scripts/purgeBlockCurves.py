#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
purgeBlockCurves.py
Deletes all curve geometry from selected block definitions (including nested ones) 
and updates the definitions in place. Skips reference blocks and reports total removed curves.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2026 in Basel, GPL3.0
Assisted by ChatGPT
"""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
import System


def cleanBlock(block_name, done=None):
    if done is None:
        done = set()

    if block_name in done:
        return 0

    done.add(block_name)

    idef = sc.doc.InstanceDefinitions.Find(block_name)
    if not idef:
        return 0

    if idef.IsReference:
        print("Skipping reference block: " + block_name)
        return 0

    rhino_objects = idef.GetObjects()
    if not rhino_objects:
        return 0

    geometry = System.Collections.Generic.List[Rhino.Geometry.GeometryBase]()
    attributes = System.Collections.Generic.List[Rhino.DocObjects.ObjectAttributes]()

    removed = 0

    for obj in rhino_objects:
        geo = obj.Geometry
        attr = obj.Attributes.Duplicate()

        if geo.ObjectType == Rhino.DocObjects.ObjectType.InstanceReference:
            child_name = obj.InstanceDefinition.Name
            if child_name:
                removed += cleanBlock(child_name, done)

        if geo.ObjectType == Rhino.DocObjects.ObjectType.Curve:
            removed += 1
            continue

        geometry.Add(geo.Duplicate())
        attributes.Add(attr)

    sc.doc.InstanceDefinitions.ModifyGeometry(idef.Index, geometry, attributes)

    return removed


def purgeBlockCurves():
    ids = rs.GetObjects("Select block instances", 4096, preselect=True)
    if not ids:
        return

    names = []
    for obj_id in ids:
        name = rs.BlockInstanceName(obj_id)
        if name and name not in names:
            names.append(name)

    total = 0
    done = set()

    for name in names:
        if name in done:
            continue
        total += cleanBlock(name, done)

    sc.doc.Views.Redraw()
    print("Removed {} curves total.".format(total))


purgeBlockCurves()