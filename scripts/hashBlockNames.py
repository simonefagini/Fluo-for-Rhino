#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
hashBlockNames.py
Renames all editable block definitions with randomly generated unique hashes.
Skips reference blocks and updates all matching definitions in place.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
April 2026 in Basel, GPL3.0
Assisted by ChatGPT
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import random
import string


def randomHash(length=8):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def hashBlockNames():
    block_names = rs.BlockNames()
    if not block_names:
        print("No blocks found.")
        return

    used_names = set(block_names)
    renamed = 0

    for name in block_names:
        idef = sc.doc.InstanceDefinitions.Find(name)
        if not idef:
            continue

        if idef.IsReference:
            print("Skipping reference block: " + name)
            continue

        new_name = None
        while True:
            candidate = randomHash()
            if candidate not in used_names:
                new_name = candidate
                used_names.add(candidate)
                break

        if sc.doc.InstanceDefinitions.Modify(idef.Index, new_name, idef.Description, False):
            print(name + " -> " + new_name)
            renamed += 1

    sc.doc.Views.Redraw()
    print("Renamed {} block definitions.".format(renamed))


hashBlockNames()