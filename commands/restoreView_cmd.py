#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
restoreView_cmd.py
A command to restore the named view tied to the active viewport by sharing the same name.
Ideal for reverting to a saved state after temporarily modifying a view while working on the model.
If the active viewport is a default view, the command takes no action.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
Dec 2024 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
from scriptcontext import doc

__commandname__ = "RestoreView"


def RestoreView():
    
    defaultViews = ["Top","Bottom","Left","Right","Front","Back","Perspective","Two Point Perspective","Parallel"]
    
    activeView = doc.Views.ActiveView.ActiveViewport.Name
    viewModeParallel = rs.ViewProjection(activeView)
    
    
    if activeView in defaultViews and viewModeParallel == 1: # 1 = parallel, 2 = perspective, 3 = two point perspective
        print("Cannot restore default views!")
        
    elif rs.RestoreNamedView(activeView) is None:
        print("View name is not a saved Named View!")
    else:
        print("View restored successfully!")
    
      
    return


def RunCommand( is_interactive ):
  
  RestoreView()
    
  return 0
    
if __name__ == "__main__":
     
    try:
        RestoreView()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")
