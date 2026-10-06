#! python 2
# -*- coding: utf-8 -*-

"""
tagDot_cmd.py
Places a single text dot at a picked point using a user-defined tag.
Designed for quick annotation and marking tasks without repetition or counting.
Written by simone fagini as part of Fluo-for-Rhino
April 2026, Basel. GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "tagDot"

def tagDot():
    tag = rs.GetString("Enter tag text", "A")
    if tag is None:
        print("User canceled...")
        return

    point = rs.GetPoint("Pick point to insert tagDot...")
    if not point:
        print("User canceled...")
        return

    dot = rs.AddTextDot(tag, point)
    rs.TextDotHeight(dot, 20)

def RunCommand(is_interactive):
    tagDot()
    return 0

if __name__ == "__main__":
    try:
        tagDot()
    except ValueError as e:
        print(e)
    except Exception as e:
        print("Something went wrong:", e)