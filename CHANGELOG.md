# Changelog

## [1.0.1] - 2026-10-22

### Added
- `tempScript` command: pick a Python script once with the `Set` option, then press Enter to run its latest saved version. It runs through `RunPythonScript`, so Python 3 scripts work too on Rhino 8. The path is remembered until Rhino is closed. The alias `temp` runs it straight away.
- `rotateReference` command: rotate objects by a reference angle, picking a line for the current direction and a line for the new one.
- `toggleClip` command: enable or disable clipping planes in the active viewport only.
- `heightDot` has a `Unit` option (mm, cm, m or the document unit), remembered during the session. The default is m.
- New aliases: `rf` (rotateReference), `tc` (toggleClip) and `temp` (tempScript).

### Fixed
- `shake` and `rotateRandom` no longer crash when a prompt is canceled.
- `blocksToParentLayer` now reports the objects it could not move, with their id and color source, instead of silently skipping them.
- `namedViewPerspective` (alias `p0`) keeps the viewport's display mode instead of forcing Shaded.
- Removed a leftover debug print from `shake`.
- The `vr` alias now ends with `_Enter`.
- The AI-assistance lines in the script headers now use the same wording.

## [1.0.0] - 2026-10-06

First tagged release of Fluo-for-Rhino: a personal collection of Rhino commands, scripts and aliases, now packaged as a ready-to-use plugin.

### Included
- 28 Python commands in `commands/` (see the [commands README](commands/README.md)).
- 9 scripts in `scripts/` (see the [scripts README](scripts/README.md)).
- The alias list in `aliases/`, with a tool to keep it sorted.
- Plugin bundle `Fluo-for-Rhino-v1.0.0.zip`, attached to the GitHub release. Unzip it and place the folder in your Rhino `PythonPlugins` folder (see the [README](README.md)). Inside the bundle the commands live in a folder called `dev`, which is the name Rhino looks for, and the scripts in `scripts`.

### Coming up
- Commands run on IronPython 2.7. Python 3 will follow once Rhino supports it for these commands.
- A toolbar is planned for v2.0.0.
