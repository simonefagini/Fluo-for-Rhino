# Testing status

What has been checked, and what is still open. Updated by hand after each test session.

## Checked
- **Rhino 7, MacOS:** all commands and scripts, including everything new in v1.1.0.
- **Rhino 8, Windows 11:** everything up to v1.0.0.

## Still to check on Rhino 8, Windows 11

New or changed since v1.0.0:
- [ ] `tempScript`: pick a file with `Set`, Enter runs it, edit the file and run again picks up the change, a moved file is reported.
- [ ] `tempScript` with a Python 3 script (`#! python 3` header). This cannot be tested on Rhino 7.
- [ ] `temp` alias (`'_tempScript _Enter`), including the very first run with no saved file.
- [ ] `heightDot`: `Unit` option with mm, cm, m and Document, in a file with non-default units (feet, inches).
- [ ] `rotateReference`
- [ ] `toggleClip`
- [ ] `namedViewPerspective` (`p0`): keeps the display mode, from a wireframe Top view and from a custom display mode.
- [ ] `shake` and `rotateRandom`: cancel at every prompt (including the axis list), then a normal run.
- [ ] `blocksToParentLayer`: object with a custom per-object color; look for "Could not move object" messages.
- [ ] `urlUpdateAliases`: new aliases `rf`, `tc`, `temp` arrive and `vr` ends with `_Enter`.

Install and release:
- [ ] Install the v1.1.0 zip on Windows: folder `Fluo-for-Rhino {df47bd45-3187-4912-8324-4b2288908bb8}` placed in `...\Rhinoceros\8.0\Plug-ins\PythonPlugins\`, Rhino restarted, version printed at start-up.
- [ ] `initializeFluo4Rhino.rvb` real run (it builds the path from `%APPDATA%`, never run in Rhino yet).

## Optional: Rhino 8, MacOS
- [ ] Install from the zip into `.../Rhinoceros/8.0/Plug-ins/PythonPlugIns/` and run a few commands.

## Later (v2.0.0)
- [ ] Import `toolbar/Fluo.rui` on Mac and Windows.
- [ ] Installer and start-up script registration.
