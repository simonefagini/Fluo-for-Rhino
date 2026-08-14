#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
randomizeUV.py
Randomizes texture mapping on selected Breps using rotation, mirroring,
and variable UV scale while leaving the geometry unchanged.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
August 2026 in Basel, GPL3.0
Vibe coded with ChatGPT — GPT-5.6 Sol by OpenAI
"""

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import random
import math

CHANNEL = 1

SCALE_MIN = 0.35
SCALE_MAX = 1.4

def randomize_uv():
    ids = rs.GetObjects(
        "Select tile Breps",
        rs.filter.surface | rs.filter.polysurface,
        preselect=True
    )

    if not ids:
        return

    angles = [0, 45, 90, 135, 180, 270]

    for obj_id in ids:
        obj = sc.doc.Objects.FindId(obj_id)
        if obj is None:
            continue

        mapping = obj.GetTextureMapping(CHANNEL)
        if mapping is None:
            mapping = Rhino.Render.TextureMapping.CreateSurfaceParameterMapping()

        angle = math.radians(random.choice(angles))
        scale = random.uniform(SCALE_MIN, SCALE_MAX)

        sx = scale * random.choice([1.0, -1.0])
        sy = scale * random.choice([1.0, -1.0])

        to_origin = Rhino.Geometry.Transform.Translation(-0.5, -0.5, 0.0)

        scale_mirror = Rhino.Geometry.Transform.Scale(
            Rhino.Geometry.Plane.WorldXY,
            sx,
            sy,
            1.0
        )

        rotation = Rhino.Geometry.Transform.Rotation(
            angle,
            Rhino.Geometry.Vector3d.ZAxis,
            Rhino.Geometry.Point3d.Origin
        )

        back = Rhino.Geometry.Transform.Translation(0.5, 0.5, 0.0)

        uv_transform = back * rotation * scale_mirror * to_origin

        mapping.UvwTransform = uv_transform
        sc.doc.Objects.ModifyTextureMapping(obj_id, CHANNEL, mapping)

    sc.doc.Views.Redraw()

randomize_uv()