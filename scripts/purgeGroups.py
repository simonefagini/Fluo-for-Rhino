#! python 2
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