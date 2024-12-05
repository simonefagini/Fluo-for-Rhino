# Rhino Commands

A collection of Python-based Rhino commands designed to enhance functionality and provide useful tools for an improved Rhino experience.

## Content

```plaintext
.
..
commands/
├── ..
├── AllPointsOn_cmd.py    
├── template_cmd.py        
└── README.md

```

- ### template_cmd.py
  A template file for creating a custom Rhino command in Python to be executed directly from the Rhino command line.

- ### AllPointsOn_cmd.py
  A custom Rhino command to merge the functionality of **_PointsOn** and **_SolidPtOn**.<br>
  Tested on Rhino v7 on MacOS 14.2.1

- ### UrlUpdateAliases_cmd.py
  A quick way to offload and then re-import all Rhino aliases from the latest version of [rhinoAliases.txt](https://github.com/simonefagini/Fluo-for-Rhino/blob/main/aliases/rhinoAliases.txt).<br>
  Requires IronPython 3 (urllib2). :warning:<br>
  Tested on Rhino v7 on MacOS 14, Rhino v8 on Windows 11.

## Adding Commands

To add a Command in Rhino on Windows:
1. Run `_EditPythonScript`
2. Click **New > Command** (to insert image)
3. Insert Code and Save
4. Relaunch Rhino
5. Run Custom Command<br>
It may require to run the command from the Rhino Python Editor one fist time) :warning:

Commands Location: `/Users/user/Library/Application Support/McNeel/Rhinoceros/7.0/Plug-ins/Plug-in-Name/` (to be double checked)


## Work in Progress

| Command Name                    | Status                       |
| ------------------------------- | ---------------------------- |
| `restoreView_cmd.py`            | :construction: In Progress.. |
| `LocalUpdateAliases_cmd.py`     | :construction: In Progress..  |
| `UrlUpdateAliases_cmd.py`       | :construction: In Progress..  |
| `ObjectsByLayer_cmd.py`         | :construction: In Progress..  |

 *Latest update on 04 Dec 2024*                      



## Useful Links
- [How to Use Scripts and Plugins](https://www.rhino3d.com/docs/guides/scripts-plugins/how-to-use/)  -  How to use scripts and plugin in Rhino
- [Rhino Developer Page](https://developer.rhino3d.com/)  - Comprehensive list of Rhino for Developer Resources
- [Rhino Command Template](https://github.com/simonefagini/Fluo-for-Rhino/blob/main/commands/template_cmd.py)  -  A template file to create a Rhino Command in Python
