#! python 2
# -*- coding: utf-8 -*-
"""
heightDot_cmd.py
Sets a quick text dot with insertion point height values, based on z-axis of current cPlane.
The unit (mm, cm, m or the document's own unit) is picked with the Unit option and remembered during the session; the default is m.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
October 2025, on a SBB Train, between Lugano and Basel. GPL3.0
"""
import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
from Rhino.Input import GetResult
from Rhino.Input.Custom import GetPoint

__commandname__ = "heightDot"

UNIT_NAMES = ["mm", "cm", "m", "Document"]
UNIT_SYSTEMS = {
	"mm": Rhino.UnitSystem.Millimeters,
	"cm": Rhino.UnitSystem.Centimeters,
	"m": Rhino.UnitSystem.Meters,
}
UNIT_DECIMALS = {"mm": 0, "cm": 1, "m": 2, "Document": 2}
STICKY_KEY = "heightDot_unit"

def systemUnit(unitValue, unitName):
	# Converts a height from document units to the chosen unit and formats it as text
	docSystem = sc.doc.ModelUnitSystem

	if unitName == "Document" or unitName not in UNIT_SYSTEMS:
		label = rs.UnitSystemName(False, False, True)
		decimals = UNIT_DECIMALS["Document"]
	else:
		unitValue = unitValue * Rhino.RhinoMath.UnitScale(docSystem, UNIT_SYSTEMS[unitName])
		label = unitName
		decimals = UNIT_DECIMALS[unitName]

	unitValue = round(unitValue, decimals)
	if decimals == 0:
		unitValue = int(unitValue)

	return str(unitValue) + " " + label

def getPoint(prompt):
	# Point pick with a sticky Unit option. Returns the point, or None for Enter/Escape.
	gp = GetPoint()
	gp.SetCommandPrompt(prompt)

	while True:
		unitName = sc.sticky.get(STICKY_KEY, "m")
		gp.ClearCommandOptions()
		gp.AddOptionList("Unit", UNIT_NAMES, UNIT_NAMES.index(unitName))

		result = gp.Get()

		if result == GetResult.Point:
			return gp.Point()

		if result == GetResult.Option:
			sc.sticky[STICKY_KEY] = UNIT_NAMES[gp.Option().CurrentListOptionIndex]
			continue

		return None

def heightDot():
	# Main code of command
	print("Running " + __commandname__ + "...")
	
	c_plane = getPoint("Pick origin or press Enter/Escape for 0,0,0")
	if not c_plane:
		c_plane = [0,0,0]

	repeat = True

	while repeat == True:

		d_origin = getPoint("Pick point to insert heightDot")
		if not d_origin:
			print("User canceled...")
			return

		d_height = d_origin[2] - c_plane[2]

		newDot = rs.AddTextDot(systemUnit(d_height, sc.sticky.get(STICKY_KEY, "m")),d_origin)
		rs.TextDotHeight(newDot, 20)
	
	return

def RunCommand( is_interactive ):
  
	heightDot()
	
	return 0
    
if __name__ == "__main__":
     
	try:
		heightDot()
	except ValueError as e:
		print(e)
	except Exception:
		print("Something went wrong...")