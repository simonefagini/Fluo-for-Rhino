#! python 2
# -*- coding: utf-8 -*-

"""
localAliasUpdate_cmd.py
Twin of urlAliasUpdate: offload and then re-import all Rhino aliases, but from an alias .txt file on your computer instead of the online one.
Useful on a fresh install, on a new machine, or to try an edited rhinoAliases.txt before it goes online.
The file is picked in a dialog, then checked first (no command for an alias, duplicate names, empty file).
If anything is wrong, nothing is changed. Otherwise ALL current aliases are deleted and replaced by the ones in the file,
so personal aliases that are not in the file are lost. The command prints how many aliases were loaded and which ones were removed.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
Vibe coded with Claude Sonnet 5.5 by Anthropic
November 2026 in Basel, GPL3.0
"""

import io
import rhinoscriptsyntax as rs

__commandname__ = "localAliasUpdate"


def ReadLines(path):
    # utf-8-sig drops the byte order mark some editors add at the start of a text file
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return f.readlines()


def ParseAliases(lines):
    """Checks every line first. Returns (pairs, errors); nothing is changed in Rhino here."""
    pairs = []
    errors = []
    seen = {}
    for number, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue  # blank lines are ignored
        parts = line.split(None, 1)
        if len(parts) < 2:
            errors.append("line " + str(number) + ": no command for '" + parts[0] + "'")
            continue
        name = parts[0].lower()
        if name in seen:
            errors.append("line " + str(number) + ": '" + name + "' already defined on line " + str(seen[name]))
            continue
        seen[name] = number
        pairs.append((name, parts[1].strip()))
    return pairs, errors


def LocalAliasUpdate():
    path = rs.OpenFileName("Select the aliases file", "Text files (*.txt)|*.txt||")
    if not path:
        print("User canceled...")
        return False

    try:
        lines = ReadLines(path)
    except Exception as e:
        print("Couldn't read " + path + ": " + str(e))
        return False

    pairs, errors = ParseAliases(lines)

    if errors:
        print("The aliases file has errors, nothing was changed:")
        for err in errors:
            print("  " + err)
        return False
    if not pairs:
        print("The aliases file is empty, nothing was changed.")
        return False

    # File is clean: now replace the aliases
    oldAliases = [name.lower() for name in (rs.AliasNames() or [])]
    newNames = set(name for name, _ in pairs)
    removed = sorted(name for name in oldAliases if name not in newNames)

    for name in oldAliases:
        rs.DeleteAlias(name)
    for name, command in pairs:
        rs.AddAlias(name, command)

    print("Aliases updated: " + str(len(pairs)) + " loaded (was " + str(len(oldAliases)) + ").")
    if removed:
        print("Removed (not in the file): " + ", ".join(removed))
    return True


def RunCommand(is_interactive):
    return 0 if LocalAliasUpdate() else 1


if __name__ == "__main__":

    try:
        LocalAliasUpdate()
    except Exception as e:
        print("Something went wrong: " + str(e))
