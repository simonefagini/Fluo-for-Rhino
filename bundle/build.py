# -*- coding: utf-8 -*-

"""
build.py
Builds the Fluo-for-Rhino plugin bundle (Fluo-for-Rhino-vX.Y.Z.zip) from the files in this repository.
Run it with a regular Python 3 from the repository root:  python bundle/build.py [output_folder]
The version is read from __version__ in commands/Fluo_cmd.py. The zip is written to ./dist by default.

Bundle layout:
  Fluo-for-Rhino {GUID}/
    dev/           all commands/*_cmd.py (the folder name Rhino looks for)
    scripts/       everything in scripts/ except its README
    CHANGELOG.md
    README.md      bundle/README.md, with the version filled in
"""

import os
import re
import sys
import zipfile

GUID = "df47bd45-3187-4912-8324-4b2288908bb8"
PLUGIN_FOLDER = "Fluo-for-Rhino {" + GUID + "}"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def readVersion():
    with open(os.path.join(ROOT, "commands", "Fluo_cmd.py"), "r") as f:
        match = re.search(r'^__version__ = "([^"]+)"', f.read(), re.MULTILINE)
    if not match:
        sys.exit("Could not find __version__ in commands/Fluo_cmd.py")
    return match.group(1)


def collectFiles(version):
    """Returns a list of (path inside the plugin folder, file bytes)."""
    files = []

    commandsDir = os.path.join(ROOT, "commands")
    for name in sorted(os.listdir(commandsDir)):
        if name.endswith("_cmd.py"):
            files.append(("dev/" + name, open(os.path.join(commandsDir, name), "rb").read()))

    scriptsDir = os.path.join(ROOT, "scripts")
    for name in sorted(os.listdir(scriptsDir)):
        if name != "README.md" and os.path.isfile(os.path.join(scriptsDir, name)):
            files.append(("scripts/" + name, open(os.path.join(scriptsDir, name), "rb").read()))

    files.append(("CHANGELOG.md", open(os.path.join(ROOT, "CHANGELOG.md"), "rb").read()))

    readme = open(os.path.join(ROOT, "bundle", "README.md"), "rb").read()
    files.append(("README.md", readme.replace(b"{version}", version.encode("utf-8"))))

    return files


def build(outDir):
    version = readVersion()
    files = collectFiles(version)

    if not os.path.isdir(outDir):
        os.makedirs(outDir)
    zipPath = os.path.join(outDir, "Fluo-for-Rhino-v" + version + ".zip")

    with zipfile.ZipFile(zipPath, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in files:
            z.writestr(PLUGIN_FOLDER + "/" + path, data)

    commands = len([p for p, _ in files if p.startswith("dev/")])
    scripts = len([p for p, _ in files if p.startswith("scripts/")])
    print("Built " + zipPath)
    print("  version " + version + ": " + str(commands) + " commands, " + str(scripts) + " scripts")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist"))
