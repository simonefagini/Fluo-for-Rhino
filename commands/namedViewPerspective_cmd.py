#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
namedViewPerspective_cmd.py
A command to temporarily switch the current view to a Perspective view, 
making it easier to orbit and navigate for an improved modeling experience.
Use the restoreView (rv) command to return to the previous Named View state.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
December 2024 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs

__commandname__ = "NamedViewPerspective"


def namedViewPerspective():
    viewID = rs.CurrentView( return_name=False )
    viewName = rs.ViewTitle(viewID)
    rs.Command("'_SetView _World _Perspective _SetDisplayMode _Shaded")
    
    rs.RenameView( viewID, viewName )
    print(viewName + " set to Perspective mode.")
    
    return



def RunCommand( is_interactive ):
  
  namedViewPerspective()
  
  return 0
    
if __name__ == "__main__":

  try:
    namedViewPerspective()
  except Exception:
    print("Something went wrong...")