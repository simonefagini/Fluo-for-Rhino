#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
heightDot_cmd.py
Sets a quick text dot to visually count elements.
Written by simone fagini as part of Fluo-for-Rhino
March 2026, Basel. GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "countingDot"

def heightDot():
    # Ask user for starting number
    counter = rs.GetInteger("Start counting from", 1)
    if counter is None:
        print("User canceled...")
        return

    while True:
        point = rs.GetPoint("Pick point to insert countingDot (Esc to stop)...")
        if not point:
            print("User canceled...")
            break

        dot = rs.AddTextDot(str(counter), point)
        rs.TextDotHeight(dot, 20)

        counter += 1

def RunCommand(is_interactive):
    heightDot()
    return 0

if __name__ == "__main__":
    try:
        heightDot()
    except ValueError as e:
        print(e)
    except Exception as e:
        print("Something went wrong:", e)