#! python 2
# -*- coding: utf-8 -*-

"""
liveDim_cmd.py
A command that shows all the measures between two points while you move the cursor, a bit like the temporary dimensions of Revit.
Pick a first point, then move: a right triangle follows the cursor, built in the active construction plane,
with a circle around its first point as wide as the horizontal length.
Live on screen: distance (D), horizontal length (L), height (H), dX, dY, the angle in the plane and the slope angle.
Click to keep the measures on screen and print them in the command line, with the running total.
The point you clicked becomes the start of the next segment, so you can go on to a third point, a fourth, and so on.
Use the Start option to begin a new chain from another point. Enter ends the command, Escape cancels it.
Nothing is created in the model: the kept measures disappear when the command ends. Values are in the document units.
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
TEXT_HEIGHT = 18  # size in pixels of every number on screen


def inkColor():
    # Black on a light viewport background, white on a dark one
    background = Rhino.ApplicationSettings.AppearanceSettings.ViewportBackgroundColor
    brightness = 0.299 * background.R + 0.587 * background.G + 0.114 * background.B
    return System.Drawing.Color.Black if brightness > 128 else System.Drawing.Color.White


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
        self.kept = []  # measured segments of this chain: (start, end)
        self.total = 0.0


def drawLabel(display, viewport, point, text, ink):
    # Text on the screen, centred on a point of the model
    screen = viewport.WorldToClient(point)
    display.Draw2dText(text, ink, Rhino.Geometry.Point2d(screen.X, screen.Y), True, TEXT_HEIGHT)


def drawSegment(display, viewport, start, end, plane, ink):
    """Right triangle with the D, L and H labels on the middle of their lines, as in Height.py."""
    m = measure(start, end, plane)
    tol = sc.doc.ModelAbsoluteTolerance

    display.DrawLine(start, end, ink, 2)
    if m["length"] > tol:
        display.DrawLine(start, m["corner"], ink, 1)
    if abs(m["height"]) > tol:
        display.DrawLine(m["corner"], end, ink, 1)

    drawLabel(display, viewport, midPoint(start, end), "D " + fmt(m["distance"]), ink)
    if m["length"] > tol:
        drawLabel(display, viewport, midPoint(start, m["corner"]), "L " + fmt(m["length"]), ink)
    if abs(m["height"]) > tol:
        drawLabel(display, viewport, midPoint(m["corner"], end), "H " + fmt(m["height"]), ink)
    return m


def onDynamicDraw(sender, e, session):
    display = e.Display
    ink = inkColor()

    # Segments already measured in this chain stay on screen
    for keptStart, keptEnd in session.kept:
        drawSegment(display, e.Viewport, keptStart, keptEnd, session.plane, ink)

    start = session.start
    end = e.CurrentPoint
    m = drawSegment(display, e.Viewport, start, end, session.plane, ink)

    # Circle around the first point of the segment, in the construction plane, as wide as the horizontal length
    if m["length"] > sc.doc.ModelAbsoluteTolerance:
        circlePlane = Rhino.Geometry.Plane(start, session.plane.XAxis, session.plane.YAxis)
        display.DrawCircle(Rhino.Geometry.Circle(circlePlane, m["length"]), ink, 1)

    # The offsets and the angles are listed next to the cursor
    lines = [
        "dX " + fmt(m["dx"]) + "   dY " + fmt(m["dy"]),
        u"Angle " + "{:.1f}".format(m["angle"]) + DEG,
        u"Slope " + "{:.1f}".format(m["slope"]) + DEG,
    ]
    screen = e.Viewport.WorldToClient(end)
    for i, text in enumerate(lines):
        display.Draw2dText(text, ink, Rhino.Geometry.Point2d(screen.X + 24, screen.Y + 24 + i * (TEXT_HEIGHT + 6)), False, TEXT_HEIGHT)


def getFirstPoint():
    gp = GetPoint()
    gp.SetCommandPrompt("Pick first point")
    if gp.Get() != GetResult.Point:
        return None
    return gp.Point()


def liveDim():
    start = getFirstPoint()
    if start is None:
        return False

    session = Session(start)
    unit = rs.UnitSystemName(False, False, True)

    while True:
        gp = GetPoint()
        gp.SetCommandPrompt("Pick next point, Enter to finish")
        gp.AcceptNothing(True)
        gp.AddOption("Start")
        gp.SetBasePoint(session.start, True)
        handler = lambda sender, e: onDynamicDraw(sender, e, session)
        gp.DynamicDraw += handler

        try:
            result = gp.Get()
        finally:
            gp.DynamicDraw -= handler

        if result == GetResult.Point:
            end = gp.Point()
            m = measure(session.start, end, session.plane)
            session.total += m["distance"]
            session.kept.append((session.start, end))
            print((u"Distance " + fmt(m["distance"]) + " | Length " + fmt(m["length"]) +
                   " | Height " + fmt(m["height"]) + " | dX " + fmt(m["dx"]) + " | dY " + fmt(m["dy"]) +
                   u" | Angle " + "{:.1f}".format(m["angle"]) + DEG +
                   u" | Slope " + "{:.1f}".format(m["slope"]) + DEG +
                   " | Total " + fmt(session.total) + " (" + unit + ")"))
            # The point just clicked is where the next segment starts
            session.start = end
            continue

        if result == GetResult.Option:
            newStart = getFirstPoint()
            if newStart is not None:
                session = Session(newStart)
            continue

        sc.doc.Views.Redraw()
        return result == GetResult.Nothing  # Enter finishes, Escape cancels


def RunCommand(is_interactive):

    return 0 if liveDim() else 1

if __name__ == "__main__":

    try:
        liveDim()
    except Exception as e:
        print("Something went wrong (" + e.__class__.__name__ + "): " + str(e))
