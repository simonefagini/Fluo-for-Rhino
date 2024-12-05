#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
template_cmd.py
Description...
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
date in place, GPL3.0
"""

import rhinoscriptsyntax as rs
#import library

__commandname__ = "Template"


def template():
      # Main code of command
      print(f"Running {__commandname__}...")
      
      return

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
  
  template()
  
  # you can optionally return a value from this function
  # to signify command result. Return values that make
  # sense are
  #   0 == success
  #   1 == cancel
  # If this function does not return a value, success is assumed
  return 0
    
if __name__ == "__main__":
     
    try:
        template()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")
