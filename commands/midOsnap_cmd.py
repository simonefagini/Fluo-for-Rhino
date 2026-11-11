#! python 2
# -*- coding: utf-8 -*-

"""
midOsnap_cmd.py
A command to toggle the Midpoint object snap on and off in Rhino.
Companion to centerOsnap: the other active osnaps are left untouched.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
November 2026 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "midOsnap"


def midOsnap():

    midValue = 2048
    actualOsnaps = rs.OsnapMode()
    midOn = actualOsnaps & midValue

    if midOn:
        newOsnaps = actualOsnaps & ~midValue
    else:
        newOsnaps = actualOsnaps | midValue

    rs.OsnapMode(newOsnaps)
    print("Midpoint osnap: " + ("off" if midOn else "on"))
    return

def RunCommand( is_interactive ):

  midOsnap()

  return 0

if __name__ == "__main__":

    try:
        midOsnap()
    except ValueError as e:
        print(e)
    except Exception:
        print("Something went wrong...")
