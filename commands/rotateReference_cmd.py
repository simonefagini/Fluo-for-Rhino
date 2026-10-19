#! python 2
# -*- coding: utf-8 -*-

"""
rotateReference_cmd.py
A command to rotate objects by a reference angle: pick a line for the current direction and a line for the new direction,
and the objects turn by the angle between the two, around the center you pick.
Rotation happens in the active construction plane.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
November 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
import math

__commandname__ = "rotateReference"


def planarAngle(startPoint, endPoint, plane):
    # Angle of the line startPoint -> endPoint, measured in the given plane
    start = rs.XformWorldToCPlane(startPoint, plane)
    end = rs.XformWorldToCPlane(endPoint, plane)
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    if math.hypot(dx, dy) < rs.UnitAbsoluteTolerance():
        return None

    return math.degrees(math.atan2(dy, dx))


def rotateReference():
    ids = rs.GetObjects("Select objects to rotate", preselect=True)
    if not ids:
        print("User canceled...")
        return

    center = rs.GetPoint("Pick rotation center")
    if not center:
        print("User canceled...")
        return

    refStart = rs.GetPoint("Reference line: pick start (current direction)")
    if not refStart:
        print("User canceled...")
        return

    refEnd = rs.GetPoint("Reference line: pick end", refStart)
    if not refEnd:
        print("User canceled...")
        return

    targetStart = rs.GetPoint("Target line: pick start (new direction)")
    if not targetStart:
        print("User canceled...")
        return

    targetEnd = rs.GetPoint("Target line: pick end", targetStart)
    if not targetEnd:
        print("User canceled...")
        return

    plane = rs.ViewCPlane()

    refAngle = planarAngle(refStart, refEnd, plane)
    if refAngle is None:
        print("Reference line has no length in the construction plane. Nothing rotated.")
        return

    targetAngle = planarAngle(targetStart, targetEnd, plane)
    if targetAngle is None:
        print("Target line has no length in the construction plane. Nothing rotated.")
        return

    # Keep the angle between -180 and 180 so the reported value reads naturally
    rotation = (targetAngle - refAngle) % 360.0
    if rotation > 180.0:
        rotation -= 360.0

    if abs(rotation) < 1e-9:
        print("Lines are already parallel. Nothing rotated.")
        return

    rs.RotateObjects(ids, center, rotation, axis=plane.ZAxis)

    print(str(len(ids)) + " object(s) rotated by " + str(round(rotation, 2)) + " degrees.")

    return


def RunCommand( is_interactive ):

    rotateReference()

    return 0

if __name__ == "__main__":

    try:
        rotateReference()
    except ValueError as e:
        print(e)
    except Exception as e:
        print("Something went wrong: " + str(e))
