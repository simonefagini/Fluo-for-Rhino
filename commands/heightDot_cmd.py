#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
heightDot_cmd.py
Sets a quick text dot with insertion point height values, based on z-axis of current cPlane.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
October 2025, on a SBB Train, between Lugano and Basel. GPL3.0
"""
import rhinoscriptsyntax as rs

__commandname__ = "heightDot"

def systemUnit(unitValue):
	system = rs.UnitSystemName(False, False, True)
	if system == "mm":
		unitValue = round(unitValue/1000,2)
		valueString = str(unitValue) + " m"

	elif system == "cm":
		unitValue = round(unitValue/100,2)
		valueString = str(unitValue) + " m"

	elif system == "m":
		unitValue = round(unitValue,2)	
		valueString = str(unitValue) + " m"

	else:
		unitValue = round(unitValue)
		valueString = str(unitValue) + " " +system

	return valueString

def heightDot():
	# Main code of command
	print(f"Running {__commandname__}...")
	
	c_plane = rs.GetPoint("Pick origin or press Enter/Escape for 0,0,0:")
	if not c_plane:
		c_plane = [0,0,0]

	repeat = True

	while repeat == True:

		d_origin = rs.GetPoint("Pick point to insert heightDot...")
		if not d_origin:
			print("User canceled...")
			return

		d_height = d_origin[2] - c_plane[2]

		newDot = rs.AddTextDot(systemUnit(d_height),d_origin)
		rs.TextDotHeight(newDot, 20)
	
	return

def RunCommand( is_interactive ):
  
	heightDot()
	
	return 0
    
if __name__ == "__main__":
     
	try:
		heightDot()
	except ValueError as e:
		print e
	except Exception:
		print("Something went wrong...")