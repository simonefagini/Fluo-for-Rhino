# Fluo for Rhino

**Fluo** is a collection of scripts and tools developed or curated over the past few years to streamline my daily Rhino and Grasshopper workflow.
  It's essentially just a personal archive.


## Content

```plaintext

Fluo-for-Rhino/
  ├── aliases/
  ├── assets/
  ├── bundle/
  ├── commands/
  ├── scripts/
  ├── LICENSE
  └── README.md
```

- ### aliases
  A directory containing aliases and tools used to keep them organized, along with utilities to make the import/export process more efficient.

- ### assets
  Images used in the guides and READMEs, plus the source file for the toolbar icons.

- ### bundle
  The README and the build script (`python bundle/build.py`) for the plugin bundle attached to each release.

- ### commands
  A collection of Python-based Rhino commands designed to enhance functionality and provide useful tools for an improved Rhino experience.

- ### scripts
  A set of Python scripts for Rhino that tackle those odd, time-consuming tasks you don’t run into every day—but hate doing by hand. 

## Adding Fluo-for-Rhino
**Fluo-for-Rhino** is also available as a ready-to-use Rhino plugin that bundles all the custom commands from this repository.
Download the latest `Fluo-for-Rhino-vX.Y.Z.zip` from the [Releases page](https://github.com/simonefagini/Fluo-for-Rhino/releases/latest) and unzip it. The folder inside is already named `Fluo-for-Rhino {df47bd45-3187-4912-8324-4b2288908bb8}`, keep that name as it is.

### Rhino for Windows
To add the full bundle to your Windows environment, place the unzipped folder in:

```plaintext
C:\Users\%username%\AppData\Roaming\McNeel\Rhinoceros\8.0\Plug-ins\PythonPlugins\
```
💡 **NOTE**: If you already have an older bundle version, replace the existing folder with the new one.

### Rhino for Mac
To add the full bundle to your Mac OS environment, place the unzipped folder in:

```plaintext
/Users/~/Library/Application Support/McNeel/Rhinoceros/8.0/Plug-ins/PythonPlugIns/
```


💡 **NOTE**: If you already have an older bundle version, replace the existing folder with the new one.

### Creating a new bundle
If you want to make your own plug-in or bundle of commands, follow the steps in the official [guide](https://developer.rhino3d.com/en/guides/rhinopython/7/creating-rhino-commands-using-python/).


## Useful Links

- [Rhinotools](https://github.com/ejnaren/rhinotools/tree/master)  –  Ejnar Brendsdal great toolbox for Rhino (included Rhino v8 by default)
- [Rhino Commands List](https://docs.mcneel.com/rhino/8/help/en-us/commandlist/command_list.htm)  –  List of all the built-in commands in Rhino 8
- [Rhino API References](https://developer.rhino3d.com/api/)  –  Comprehensive documentations for Rhino and Grasshopper (RhinoCommon, RhinoScriptSyntax, etc.)
- [RhinoCommon in Python](https://developer.rhino3d.com/guides/rhinopython/using-rhinocommon-from-python/)  -  HowTo use RhinoCommon inside of a Python Script



## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

![License: GPL-3.0](https://img.shields.io/badge/License-GPL%20v3-blue.svg)
