#! python 2
# -*- coding: utf-8 -*-

"""
purgeGroups.py
Ungroups all the objects in the file, so no groups are left.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
May 2026 in Basel, GPL3.0
Vibe coded with GPT-5.5 by OpenAI
"""

import rhinoscriptsyntax as rs

def ungroupAll():
    groups = rs.GroupNames()
    if not groups:
        print("No groups found.")
        return

    count = 0

    for g in groups:
        objs = rs.ObjectsByGroup(g)
        if objs:
            rs.RemoveObjectsFromGroup(objs, g)
            count += 1

    print("Ungrouped {} groups.".format(count))

ungroupAll()