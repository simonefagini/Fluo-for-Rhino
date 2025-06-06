#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fluo.py
Initialize the Fluo-for-Rhino pack at every Rhino start up. Must be idle with a Visual Basic Rhino Script.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
June 2025 in Basel, GPL3.0
"""

import rhinoscriptsyntax as rs
#import library

__commandname__ = "Fluo"


def Fluo():
    
      import time
      print("Initializing Fluo-for-Rhino...")
      time.sleep(2)
      
      print("Fluo-for-Rhino v.01")
      
      return


def RunCommand( is_interactive ):
  
  Fluo()
  return 0
    
if __name__ == "__main__":
     
    try:
        Fluo()
    except ValueError as e:
        print e
    except Exception:
        print("Something went wrong...")