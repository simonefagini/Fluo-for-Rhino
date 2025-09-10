#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
clickCounter.py
Sequential numbering by click. Fast manual enumeration for any workflow.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
September 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "clickCounter"


def clickCounter():
    import rhinoscriptsyntax as rs
    import math

    def get_text_multipliers(radius, coeff=0.7):

        temp_texts = []
        digits_examples = [("8", 1), ("88", 2), ("888", 3)]
        multipliers = {}

        for txt, d in digits_examples:
            temp = rs.AddText(txt, [0, 0, 0], height=1)
            temp_texts.append(temp)
            bbox = rs.BoundingBox(temp)
            width = rs.Distance(bbox[0], bbox[1])
            height = rs.Distance(bbox[0], bbox[3])
            multipliers[d] = coeff * (radius * 2) / max(width, height)

        for t in temp_texts:
            rs.DeleteObject(t)

        return multipliers

    def numbered_circles():
        counter = 1
        created_objects = []

        rs.AddLayer("_ANNO")
        rs.CurrentLayer("_ANNO")

        # pick two points once
        ptA = rs.GetPoint("Pick first point for radius")
        if not ptA:
            return
        ptB = rs.GetPoint("Pick second point for radius")
        if not ptB:
            return
        radius = math.ceil(rs.Distance(ptA, ptB))

        multipliers = get_text_multipliers(radius, coeff=0.7)

        while True:
            pt = rs.GetPoint("Pick point for numbered circle (ESC to stop)")
            if not pt:
                break

            circle = rs.AddCircle(pt, radius)
            created_objects.append(circle)

            digits = len(str(counter))
            if digits == 1:
                text_height = multipliers[1]
            elif digits == 2:
                text_height = multipliers[2]
            else:
                text_height = multipliers[3]

            text = rs.AddText(
                str(counter), pt, height=text_height, justification=2 + 131072
            )
            created_objects.append(text)
            counter += 1

        if created_objects:

            base_name = "NumberedCircles"
            block_name = base_name
            counter_name = 1
            while rs.IsBlock(block_name):
                counter_name += 1
                block_name = base_name + "_" + str(counter_name)

            rs.AddBlock(created_objects, [0, 0, 0], block_name, delete_input=True)
            rs.InsertBlock(block_name, [0, 0, 0])
            print(
                "Block created: "
                + block_name
                + " with "
                + str(len(created_objects))
                + " objects"
            )

    numbered_circles()
    return


def RunCommand(is_interactive):
    clickCounter()
    return 0


if __name__ == "__main__":

    try:
        clickCounter()
    except ValueError as e:
        print(e)
    except Exception:
        print("Something went wrong...")
