#! python 2
# -*- coding: utf-8 -*-

"""
urlUpdateAliases_cmd.py
A quick way to offload and then re-import all Rhino aliases from the latest version of rhinoAliases.txt.
The online file is downloaded and checked first (no command for an alias, duplicate names, empty file).
If anything is wrong, nothing is changed. Otherwise ALL current aliases are deleted and replaced by the online list,
so personal aliases that are not in rhinoAliases.txt are lost. The command prints how many aliases were loaded and which ones were removed.
A timestamp is added to the URL because GitHub caches the raw file for about 5 minutes.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
December 2024 in Basel, GPL3.0
Vibe coded with Claude Sonnet 5.5 by Anthropic
"""

import rhinoscriptsyntax as rs
import time
import urllib2

__commandname__ = "urlUpdateAliases"

ALIASES_URL = ("https://raw.githubusercontent.com/simonefagini/Fluo-for-Rhino/"
               "refs/heads/main/aliases/rhinoAliases.txt")


def FetchLines():
    # Timestamp query avoids GitHub's ~5 min cache of the raw file
    url = ALIASES_URL + "?t=" + str(int(time.time()))
    response = urllib2.urlopen(url, timeout=10)
    return [line.decode("utf-8") for line in response.readlines()]


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


def UrlUpdateAliases():
    try:
        lines = FetchLines()
    except Exception as e:
        print("Couldn't download rhinoAliases.txt: " + str(e))
        return False

    pairs, errors = ParseAliases(lines)

    if errors:
        print("rhinoAliases.txt has errors, nothing was changed:")
        for err in errors:
            print("  " + err)
        return False
    if not pairs:
        print("rhinoAliases.txt is empty, nothing was changed.")
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
        print("Removed (not in online file): " + ", ".join(removed))
    return True


def RunCommand(is_interactive):
    return 0 if UrlUpdateAliases() else 1


if __name__ == "__main__":

    try:
        UrlUpdateAliases()
    except Exception as e:
        print("Something went wrong: " + str(e))
