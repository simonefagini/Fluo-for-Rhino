#! python 2
# -*- coding: utf-8 -*-

"""
liveDim_cmd.py
A command that shows all the measures between two points while you move the cursor, a bit like the temporary dimensions of Revit.
Pick a first point, then move: a right triangle follows the cursor, built in the active construction plane.
Live on screen: distance (D), horizontal length (L), height (H), dX, dY, the angle in the plane and the slope angle.
Click to print the measures in the command line; the first point stays, so you can keep measuring from it.
Use the Start option to pick a new first point. Enter or Escape ends the command.
Nothing is created in the model. Values are in the document units.
Inspired by Height.py from LandArchTools-for-Rhino by Thomas Chapman (https://github.com/TSRChapman/LandArchTools-for-Rhino)
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
Vibe coded with Claude Sonnet 5.5 by Anthropic
November 2026 in Basel, GPL3.0
"""

import math
import System.Drawing
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
from Rhino.Geometry import Point3d, Vector3d
from Rhino.Input import GetResult
from Rhino.Input.Custom import GetPoint

__commandname__ = "liveDim"

DEG = u"°"
LINE_COLOR = System.Drawing.Color.FromArgb(40, 40, 40)
DOT_FILL = System.Drawing.Color.FromArgb(235, 235, 235)
DOT_TEXT = System.Drawing.Color.Black
TEXT_COLOR = System.Drawing.Color.FromArgb(30, 30, 30)


def measure(start, end, plane):
    """All the measures between two points, read along the axes of the given plane."""
    vec = end - start
    dx = Vector3d.Multiply(vec, plane.XAxis)
    dy = Vector3d.Multiply(vec, plane.YAxis)
    dz = Vector3d.Multiply(vec, plane.ZAxis)
    length = math.hypot(dx, dy)

    return {
        "dx": dx,
        "dy": dy,
        "height": dz,
        "length": length,
        "distance": vec.Length,
        # direction in the plane, 0-360 from the plane's X axis
        "angle": math.degrees(math.atan2(dy, dx)) % 360.0,
        # slope of the line against the plane, positive upwards
        "slope": math.degrees(math.atan2(dz, length)),
        # the corner of the right triangle, straight below or above the end point
        "corner": start + plane.XAxis * dx + plane.YAxis * dy,
    }


def fmt(value):
    return "{:.2f}".format(value)


def midPoint(a, b):
    return Point3d((a.X + b.X) / 2.0, (a.Y + b.Y) / 2.0, (a.Z + b.Z) / 2.0)


def activePlane():
    view = sc.doc.Views.ActiveView
    return view.ActiveViewport.ConstructionPlane()


class Session(object):
    # Shared between the point getter and its draw event
    def __init__(self, start):
        self.start = start
        self.plane = activePlane()


def onDynamicDraw(sender, e, session):
    start = session.start
    end = e.CurrentPoint
    m = measure(start, end, session.plane)
    display = e.Display

    display.DrawLine(start, end, LINE_COLOR, 2)
    if m["length"] > sc.doc.ModelAbsoluteTolerance:
        display.DrawLine(start, m["corner"], LINE_COLOR, 1)
    if abs(m["height"]) > sc.doc.ModelAbsoluteTolerance:
        display.DrawLine(m["corner"], end, LINE_COLOR, 1)

    # D, L and H sit on the middle of their lines, as in Height.py
    display.DrawDot(midPoint(start, end), "D " + fmt(m["distance"]), DOT_FILL, DOT_TEXT)
    if m["length"] > sc.doc.ModelAbsoluteTolerance:
        display.DrawDot(midPoint(start, m["corner"]), "L " + fmt(m["length"]), DOT_FILL, DOT_TEXT)
    if abs(m["height"]) > sc.doc.ModelAbsoluteTolerance:
        display.DrawDot(midPoint(m["corner"], end), "H " + fmt(m["height"]), DOT_FILL, DOT_TEXT)

    # The angles and the plane offsets are listed next to the cursor
    lines = [
        "dX " + fmt(m["dx"]) + "   dY " + fmt(m["dy"]),
        u"Angle " + "{:.1f}".format(m["angle"]) + DEG,
        u"Slope " + "{:.1f}".format(m["slope"]) + DEG,
    ]
    screen = e.Viewport.WorldToClient(end)
    for i, text in enumerate(lines):
        display.Draw2dText(text, TEXT_COLOR, Rhino.Geometry.Point2d(screen.X + 24, screen.Y + 24 + i * 18), False, 14)


def getFirstPoint():
    gp = GetPoint()
    gp.SetCommandPrompt("Pick first point")
    if gp.Get() != GetResult.Point:
        return None
    return gp.Point()


def liveDim():
    start = getFirstPoint()
    if start is None:
        return

    session = Session(start)

    while True:
        gp = GetPoint()
        gp.SetCommandPrompt("Pick second point, Enter to finish")
        gp.AcceptNothing(True)
        gp.AddOption("Start")
        gp.SetBasePoint(session.start, True)
        gp.DynamicDraw += lambda sender, e: onDynamicDraw(sender, e, session)

        result = gp.Get()

        if result == GetResult.Point:
            m = measure(session.start, gp.Point(), session.plane)
            unit = rs.UnitSystemName(False, False, True)
            print(("Distance " + fmt(m["distance"]) + " | Length " + fmt(m["length"]) +
                   " | Height " + fmt(m["height"]) + " | dX " + fmt(m["dx"]) + " | dY " + fmt(m["dy"]) +
                   u" | Angle " + "{:.1f}".format(m["angle"]) + DEG +
                   u" | Slope " + "{:.1f}".format(m["slope"]) + DEG + " (" + unit + ")"))
            continue

        if result == GetResult.Option:
            newStart = getFirstPoint()
            if newStart is not None:
                session.start = newStart
                session.plane = activePlane()
            continue

        return  # Enter or Escape


def RunCommand(is_interactive):

    liveDim()

    return 0

if __name__ == "__main__":

    try:
        liveDim()
    except Exception as e:
        print("Something went wrong: " + str(e))
