# Fluo for Rhino

**Fluo** is a collection of scripts and tools developed or curated over the past few years to streamline my daily Rhino and Grasshopper workflow.
  It's essentially just a personal archive.


## Content

```plaintext

Fluo-for-Rhino/
  ├── Fluo-for-Rhino {df47bd45-3187-4912-8324-4b2288908bb8}.zip
  ├── aliases/
  ├── commands/
  ├── scripts/
  ├── LICENSE
  └── README.md
```

- ### Fluo-for-Rhino {df47bd45-3187-4912-8324-4b2288908bb8}.zip 
   A Rhino plugin that bundles all the custom commands from this repository into a ready-to-use package — simply download, unzip, and place it in the correct folder.

- ### aliases
  A directory containing aliases and tools used to keep them organized, along with utilities to make the import/export process more efficient.

- ### commands
  A collection of Python-based Rhino commands designed to enhance functionality and provide useful tools for an improved Rhino experience.

- ### scripts
  A set of Python scripts for Rhino that tackle those odd, time-consuming tasks you don’t run into every day—but hate doing by hand. 

## Adding Fluo-for-Rhino
### Rhino for Windows
To add the full bundle of **Fluo-for-Rhino** to your Windows environment, download the .zip file, unzip it, and add the main folder to:

```plaintext
C:\Users\%username%\AppData\Roaming\McNeel\Rhinoceros\8.0\Plug-ins\PythonPlugins\
```
💡 **NOTE**: If you already have an older bundle version, replace the existing folder with the new one.

### Rhino for Mac
To add the full bundle of **Fluo-for-Rhino** to your Mac OS environment, download the .zip file, unzip it, and add the main folder to:

```plaintext
/Users/~/Library/Application Support/McNeel/Rhinoceros/8.0/Plug-ins/PythonPlugIns/
```


💡 **NOTE**: If you already have an older bundle version, replace the existing folder with the new one.

### Creating a new bundle
If you want to make your own plug-in or bundle of commands, follow the steps in the short [guide](/commands/AddingPlugins.md).


## Useful Links

- [Rhinotools](https://github.com/ejnaren/rhinotools/tree/master)  –  Ejnar Brendsdal great toolbox for Rhino (included Rhino v8 by default)
- [Rhino Commands List](https://docs.mcneel.com/rhino/8/help/en-us/commandlist/command_list.htm)  –  List of all the built-in commands in Rhino 8
- [Rhino API References](https://developer.rhino3d.com/api/)  –  Comprehensive documentations for Rhino and Grasshopper (RhinoCommon, RhinoScriptSyntax, etc.)
- [RhinoCommon in Python](https://developer.rhino3d.com/guides/rhinopython/using-rhinocommon-from-python/)  -  HowTo use RhinoCommon inside of a Python Script



## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

![License: GPL-3.0](https://img.shields.io/badge/License-GPL%20v3-blue.svg)
