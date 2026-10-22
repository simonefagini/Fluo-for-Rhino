# -*- coding: utf-8 -*-

"""
build_rui.py
Builds the Fluo toolbar (toolbar/Fluo.rui) from the GROUPS below.
Run it with a regular Python 3 from the repository root:  python bundle/build_rui.py
Every id is derived from a name, so each build writes the same file:
re-importing an updated Fluo.rui replaces the toolbar instead of adding a second one.
Groups are split by Rhino's own spacer item.
Icons: one SVG per command in toolbar/icons/<command>.svg, drawn on a 48x48 viewBox.
A command without a file gets a placeholder circle in its group colour.
Run with --placeholders to write those circles out as files, without touching existing ones.
Rhino 8 reads icons from <icons> (SVG, light and dark version, linked by the macro's bitmap_id).
The PNG strips in <bitmaps> are group-colour circles, a fallback for older Rhinos only.
No packages needed.
"""

import base64
import os
import re
import struct
import sys
import uuid
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "toolbar", "Fluo.rui")
ICONS_DIR = os.path.join(ROOT, "toolbar", "icons")

ICON_SIZES = [("small_bitmap", 16), ("normal_bitmap", 24), ("large_bitmap", 32)]

# (group name, placeholder colour, [(left click, right click or None)])
GROUPS = [
    ("View", "#3B82F6", [
        ("axo", "deaxo"),
        ("namedViewPerspective", "restoreView"),
        ("toggleClip", None),
        ("centerOsnap", None),
    ]),
    ("Transform", "#F97316", [
        ("moveVertical", "copyVertical"),
        ("rotateReference", None),
        ("pastePoint", None),
    ]),
    ("Variation", "#D946EF", [
        ("shake", "unshake"),
        ("rotateRandom", None),
        ("keep", None),
    ]),
    ("Annotate", "#22C55E", [
        ("tagDot", None),
        ("heightDot", None),
        ("countingDot", None),
        ("clickCounter", None),
    ]),
    ("Layers & blocks", "#EAB308", [
        ("objectsByLayer", "blocksByLayer"),
        ("blocksToParentLayer", None),
        ("whichMaterial", None),
        ("count", None),
    ]),
    ("Model & export", "#EF4444", [
        ("allPointsOn", None),
        ("dupAllBorder", None),
        ("parapet", None),
        ("dwg", None),
    ]),
    ("Setup", "#9CA3AF", [
        ("urlUpdateAliases", None),
        ("tempScript", None),
    ]),
]


def stableId(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/simonefagini/Fluo-for-Rhino/toolbar/" + name))


def readCommandNames():
    names = set()
    commandsDir = os.path.join(ROOT, "commands")
    for fileName in os.listdir(commandsDir):
        if fileName.endswith("_cmd.py"):
            with open(os.path.join(commandsDir, fileName), "r") as f:
                match = re.search(r'^__commandname__ = "([^"]+)"', f.read(), re.MULTILINE)
            if match:
                names.add(match.group(1))
    return names


def commandsInOrder():
    """Returns [(command name, group colour)] in toolbar order, after checking every name."""
    commands = []
    for _, color, buttons in GROUPS:
        for left, right in buttons:
            commands.append((left, color))
            if right:
                commands.append((right, color))

    names = [name for name, _ in commands]
    known = readCommandNames()
    missing = [name for name in names if name not in known]
    if missing:
        sys.exit("Not a command in commands/: " + ", ".join(missing))
    duplicates = sorted(set(name for name in names if names.count(name) > 1))
    if duplicates:
        sys.exit("Used twice in GROUPS: " + ", ".join(duplicates))
    return commands


# ---------- placeholder icons ----------

def circlePixels(size, color):
    """RGBA rows of an anti-aliased filled circle on a transparent square."""
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    radius = size * 0.40
    center = size / 2.0
    samples = 4
    rows = []
    for y in range(size):
        row = bytearray()
        for x in range(size):
            inside = 0
            for sy in range(samples):
                for sx in range(samples):
                    px = x + (sx + 0.5) / samples - center
                    py = y + (sy + 0.5) / samples - center
                    if px * px + py * py <= radius * radius:
                        inside += 1
            row += bytes([r, g, b, int(255 * inside / (samples * samples))])
        rows.append(bytes(row))
    return rows


def pngBase64(width, rows):
    """Encodes RGBA rows as a base64 PNG."""
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + row for row in rows)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, len(rows), 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    return base64.b64encode(png).decode("ascii")


def iconStrip(size, commands):
    """One vertical strip per size: icon i sits at index i, top to bottom."""
    rows = []
    for _, color in commands:
        rows += circlePixels(size, color)
    return pngBase64(size, rows)


def svgIcon(color):
    """A 48x48 SVG in the shape Rhino 8 writes itself. Same colour in light and dark mode."""
    return ('<svg width="48" height="48" version="1.1" xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0pt 0pt 48pt 48pt">\n'
            '  <circle fill="' + color + '" r="19.2" cx="24" cy="24" />\n'
            '</svg>')


def iconPath(name):
    return os.path.join(ICONS_DIR, name + ".svg")


def readIcon(name, color):
    """The command's SVG file, cleaned up to sit inside the .rui, or the placeholder circle."""
    path = iconPath(name)
    if not os.path.isfile(path):
        return svgIcon(color), False
    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()
    svg = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>|<!--.*?-->", "", svg, flags=re.S).strip()
    if not svg.startswith("<svg"):
        sys.exit("Not an SVG: " + path)
    if not re.search(r'viewBox="0(pt)? 0(pt)? 48(pt)? 48(pt)?"', svg):
        print("  warning: " + name + ".svg is not on a 48x48 viewBox, it may look the wrong size in Rhino")
    return svg, True


def writePlaceholders(commands):
    if not os.path.isdir(ICONS_DIR):
        os.makedirs(ICONS_DIR)
    written = 0
    for name, color in commands:
        if not os.path.isfile(iconPath(name)):
            with open(iconPath(name), "w", encoding="utf-8", newline="\n") as f:
                f.write(svgIcon(color) + "\n")
            written += 1
    print("Wrote " + str(written) + " placeholder icons to " + ICONS_DIR)


# ---------- rui ----------

def text(indent, value):
    return [indent + "<text>", indent + "  <locale_1033>" + value + "</locale_1033>", indent + "</text>"]


def buildRui():
    commands = commandsInOrder()

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<RhinoUI major_ver="5" minor_ver="0" guid="' + stableId("file") + '" localize="False" default_language_id="1033" dpi_scale="100">',
        "  <tool_bar_groups />",
        "  <tool_bars>",
        '    <tool_bar guid="' + stableId("bar/Fluo") + '">',
    ]
    lines += text("      ", "Fluo")

    for index, (groupName, _, buttons) in enumerate(GROUPS):
        if index > 0:
            lines.append('      <tool_bar_item guid="' + stableId("separator/" + groupName) + '" button_style="spacer" />')
        for left, right in buttons:
            lines.append('      <tool_bar_item guid="' + stableId("button/" + left) + '">')
            lines.append("        <left_macro_id>" + stableId("macro/" + left) + "</left_macro_id>")
            if right:
                lines.append("        <right_macro_id>" + stableId("macro/" + right) + "</right_macro_id>")
            lines.append("      </tool_bar_item>")

    lines += ["    </tool_bar>", "  </tool_bars>", "  <macros>"]

    for name, _ in commands:
        lines.append('    <macro_item guid="' + stableId("macro/" + name) + '" bitmap_id="' + stableId("bitmap/" + name) + '">')
        lines += text("      ", name)
        lines.append("      <script>! _" + name + "</script>")
        lines.append("    </macro_item>")

    lines += ["  </macros>", "  <icons>"]
    fromFiles = 0
    for name, color in commands:
        iconId = stableId("bitmap/" + name)
        svg, fromFile = readIcon(name, color)
        fromFiles += fromFile
        lines.append('    <icon guid="' + iconId + '" name="' + iconId + '.svg">')
        lines.append("      <light>" + svg + "</light>")
        lines.append("      <dark>" + svg + "</dark>")
        lines.append("    </icon>")

    lines += ["  </icons>", "  <bitmaps>"]
    for tag, size in ICON_SIZES:
        lines.append("    <" + tag + ' item_width="' + str(size) + '" item_height="' + str(size) + '">')
        lines.append("      <bitmap>" + iconStrip(size, commands) + "</bitmap>")
        lines.append("    </" + tag + ">")
    for index, (name, _) in enumerate(commands):
        lines.append('    <bitmap_item guid="' + stableId("bitmap/" + name) + '" index="' + str(index) + '" />')

    lines += [
        "  </bitmaps>",
        "  <scripts />",
        "</RhinoUI>",
    ]
    return "\n".join(lines) + "\n", commands, fromFiles


def build():
    if "--placeholders" in sys.argv:
        writePlaceholders(commandsInOrder())
    rui, commands, fromFiles = buildRui()
    with open(OUTPUT, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(rui)
    buttons = sum(len(group[2]) for group in GROUPS)
    print("Built " + OUTPUT)
    print("  " + str(buttons) + " buttons, " + str(len(commands)) + " commands, "
          + str(len(GROUPS)) + " groups, " + str(len(GROUPS) - 1) + " separators")
    print("  icons: " + str(fromFiles) + " from toolbar/icons, " + str(len(commands) - fromFiles) + " placeholders")


if __name__ == "__main__":
    build()
