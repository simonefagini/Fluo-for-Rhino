#! python 2
# -*- coding: utf-8 -*-

"""
tempScript_cmd.py
A command to run a Python script you are working on, without browsing for it every time.
Pick the script once with the Set option, then press Enter to run its latest saved version.
The script runs through RunPythonScript, so it keeps its own engine: Python 3 scripts work too.
The path is remembered until Rhino is closed. Cancelling the file dialog keeps the previous script.
If the saved script has been moved or deleted, the command says so and opens the file dialog again.
Aliases: temp runs the saved script at once ('_tempScript _Enter), resettemp opens the file dialog to pick another one ('_tempScript _Set).
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
October 2026 in Basel, GPL3.0
"""

import os
import rhinoscriptsyntax as rs
import scriptcontext as sc
from Rhino.Input import GetResult
from Rhino.Input.Custom import GetOption

__commandname__ = "tempScript"

STICKY_KEY = "tempScript_path"


def pickScript():
    # Returns the new path, or None if the dialog was cancelled (the saved path is left as it was)
    path = rs.OpenFileName("Select the script to run", "Python files (*.py)|*.py||")
    if path:
        sc.sticky[STICKY_KEY] = path
    return path


def runScript(path):
    print("Running " + os.path.basename(path) + "...")
    rs.Command('-_RunPythonScript "' + path + '"')


def temp():
    path = sc.sticky.get(STICKY_KEY)

    # First run, or the saved file is gone: ask for a script before anything else
    if not path or not os.path.isfile(path):
        if path:
            print("Script not found: " + path)
        if not pickScript():
            return

    while True:
        path = sc.sticky[STICKY_KEY]

        # Enter runs the script, Set picks another one and asks again
        go = GetOption()
        go.SetCommandPrompt("Press Enter to run " + os.path.basename(path))
        go.AcceptNothing(True)
        go.AddOption("Set")
        result = go.Get()

        if result == GetResult.Nothing:
            if os.path.isfile(path):
                runScript(path)
            else:
                print("Script not found: " + path)
            return

        if result == GetResult.Option:
            pickScript()
            continue

        return  # Cancelled


# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):

    temp()

    return 0

if __name__ == "__main__":

    try:
        temp()
    except ValueError as e:
        print(e)
    except Exception:
        print("Something went wrong...")
