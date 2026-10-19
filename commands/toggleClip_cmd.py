#! python 2
# -*- coding: utf-8 -*-

"""
toggleClip_cmd.py
A command to enable or disable clipping planes in the active viewport only, leaving every other view untouched.
Pick clipping planes, use the Name option (wildcards allowed, e.g. Sec_*) to reach hidden ones, or press Enter to act on all of them.
If any target plane already clips the active viewport, all targets are disabled there; otherwise all are enabled.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
October 2026 in Basel, GPL3.0
Vibe coded with Claude Opus 5.5 by Anthropic
"""

import rhinoscriptsyntax as rs
import Rhino
import fnmatch
from scriptcontext import doc
from Rhino.DocObjects import ObjectType, ObjectEnumeratorSettings, ClippingPlaneObject
from Rhino.Input import GetResult

__commandname__ = "toggleClip"


def AllClipPlanes():
    # Includes hidden and locked planes
    settings = ObjectEnumeratorSettings()
    settings.ObjectTypeFilter = ObjectType.ClipPlane
    settings.NormalObjects = True
    settings.LockedObjects = True
    settings.HiddenObjects = True
    return list(doc.Objects.GetObjectList(settings))


def FindByName(pattern):
    # Case-insensitive, wildcards allowed
    pattern = pattern.lower()
    return [o for o in AllClipPlanes()
            if o.Attributes.Name and fnmatch.fnmatch(o.Attributes.Name.lower(), pattern)]


def GetTargets():
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt("Select clipping planes to toggle <Enter for all>")
    go.GeometryFilter = ObjectType.ClipPlane
    go.EnablePreSelect(True, True)
    go.AcceptNothing(True)
    go.AddOption("Name")

    while True:
        result = go.GetMultiple(0, 0)

        if result == GetResult.Object:
            return [go.Object(i).Object() for i in range(go.ObjectCount)]

        if result == GetResult.Nothing:
            return AllClipPlanes()

        if result == GetResult.Option:
            name = rs.GetString("Clipping plane name (wildcards ok)")
            objs = FindByName(name) if name else []
            if objs:
                return objs
            print("No match, try again!")
            continue

        return None # Cancelled


def ClipsViewport(clipObj, viewportId):
    return any(g == viewportId for g in clipObj.ClippingPlaneGeometry.ViewportIds())


def ToggleClip():

    view = doc.Views.ActiveView
    if view is None:
        print("No active view!")
        return 1

    # ActiveViewport is the active detail when working inside a layout
    viewport = view.ActiveViewport

    targets = GetTargets()
    if targets is None:
        return 1

    targets = [o for o in targets if isinstance(o, ClippingPlaneObject)]
    if not targets:
        print("No clipping planes found!")
        return 0

    disable = any(ClipsViewport(o, viewport.Id) for o in targets)
    ids = [o.Id for o in targets]
    count = 0

    for objId in ids:
        obj = doc.Objects.FindId(objId)
        label = obj.Attributes.Name or str(objId)

        # Hidden objects don't reliably commit: show, toggle, hide again
        wasHidden = obj.IsHidden
        if wasHidden:
            doc.Objects.Show(objId, True)
            obj = doc.Objects.FindId(objId)

        if not doc.Layers[obj.Attributes.LayerIndex].IsVisible:
            print("Note: '" + label + "' is on a hidden layer")

        if disable:
            done = obj.RemoveClipViewport(viewport, True)
        else:
            done = obj.AddClipViewport(viewport, True)

        if wasHidden:
            doc.Objects.Hide(objId, True)

        if done:
            count += 1
        else:
            print("Failed on '" + label + "'")

    doc.Objects.UnselectAll()
    doc.Views.Redraw()

    action = "Disabled" if disable else "Enabled"
    print(action + " " + str(count) + "/" + str(len(ids)) + " clipping plane(s) in " + viewport.Name)

    return 0


def RunCommand( is_interactive ):

    return ToggleClip()

if __name__ == "__main__":

    try:
        ToggleClip()
    except ValueError as e:
        print(e)
    except Exception:
        print("Something went wrong...")
