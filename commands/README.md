# Rhino Commands

A collection of Python-based Rhino commands designed to enhance functionality and provide useful tools for an improved Rhino experience.

## Content

```plaintext
.
..
commands/
├── ..
├── dupAllBorder_cmd.py
├── moveVertical_cmd.py
├── namedViewPerspective_cmd.py
├── urlUpdateAliases_cmd.py
├── obejctsByLayer_cmd.py
├── restoreView_cmd.py
├── allPointsOn_cmd.py    
├── template_cmd.py
├── Fluo-for-Rhino {df47bd45-3187-4912-8324-4b2288908bb8}.zip
├── AddingPlugins.md    
└── README.md
```

- ### Fluo-for-Rhino {df47bd45-3187-4912-8324-4b2288908bb8}.zip 
   A Rhino plugin that bundles all the custom commands from this repository into a ready-to-use package — simply download, unzip, and place it in the correct folder.
  
- ### template_cmd.py
  A template file for creating a custom Rhino command in Python to be executed directly from the Rhino command line.

- ### allPointsOn_cmd.py
  A custom Rhino command to merge the functionality of **_PointsOn** and **_SolidPtOn**.<br>
  Tested on Rhino v7 on MacOS 14.2.1 and Rhino v8 on Windows 11.

- ### restoreView_cmd.py
  A command to restore the named view tied to the active viewport by sharing the same name.
  Ideal for reverting to a saved state after temporarily modifying a view while working on the model.
  If the active viewport is a default view, the command takes no action.<br>
  Tested on Rhino v7 on MacOS 14.2.1 and Rhino v8 on Windows 11.

- ### objectsByLayer_cmd.py
  A command to set the properties of the selected object to "By Layer".<br>
  Targeted properties: Object Color, Material, Linetype, Print Color, and Print Width.<br>
  Tested on Rhino v7 on MacOS 14.2.1 and Rhino v8 on Windows 11.
  
- ### urlUpdateAliases_cmd.py
  A quick way to offload and then re-import all Rhino aliases from the latest version of [rhinoAliases.txt](/aliases/rhinoAliases.txt).<br>
  Requires IronPython 3 (urllib2). :warning:<br>
  Tested on Rhino v7 on MacOS 14 and Rhino v8 on Windows 11.

- ### namedViewPerspective_cmd.py
  A command to temporarily switch the current view to a Perspective view, making it easier to orbit and navigate for an improved modeling experience.
  Use the [restoreView (rv)](/commands/restoreView_cmd.py) command to return to the previous Named View state. <br>
  Tested on Rhino v8 on Windows 11.

- ### moveVertical_cmd.py
  A command to improve the Move Vertical workflow by preventing Project snap interference when executing the command. <br>
  Tested on Rhino v7 on MacOS 14 and Rhino v8 on Windows 11.

- ### dupAllBorder_cmd.py
  A custom Rhino command to merge the functionality of 'DupBorder and 'DupFaceBorder. <br>
  It does not support the preselection of Brep faces. :warning:<br>
  Tested on Rhino v7 on MacOS 14 and Rhino v8 on Windows 11.

- ### centerOsnapToggle_cmd.py
    A command to toggle the **Center** object snap on and off in Rhino. <br>
    This provides a quick way to enable or disable snapping to the center of circles and arcs during modeling.

   The command modifies the targeted osnap setting using **bitwise operations** to preserve the state of other active osnaps.

   #### List of osnap values:
   ```
   0           None  
   2           Near  
   8           Focus  
   32          Center  
   64          Vertex  
   128         Knot  
   512         Quadrant  
   2048        Midpoint  
   8192        Intersection  
   0x20000     End (or 131072)  
   0x80000     Perpendicular (or 524288)  
   0x200000    Tangent (or 2097152)  
   0x8000000   Point (or 8388608)
   ```
   Tested on Rhino v7 on MacOS 14 and Rhino v8 on Windows 11.

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

## Work in Progress

| Command Name                    | Status                       |
| ------------------------------- | ---------------------------- |
| `batchSwitchLayersMaterials_cmd.py`           | :bulb: Planned..  |
| `centerOSnap_cmd.py`           | :bulb: Planned..  |
| `RotateRandom_cmd.py`           | :construction: In Progress..  |
| `UnselRandom_cmd.py`            | :construction: In Progress..  |
| `UrlUpdateAliases_cmd.py`       | :test_tube: Needs Testing  |

 *Latest update on 18 Dec 2024*                      


## Useful Links
- [Creating Rhino Commands Using Python](https://developer.rhino3d.com/en/guides/rhinopython/7/creating-rhino-commands-using-python/)  -  Rhino Developers official guide on how to create Rhino commands from Python scripts
- [How to Use Scripts and Plugins](https://www.rhino3d.com/docs/guides/scripts-plugins/how-to-use/)  -  How to use scripts and plugin in Rhino
- [Rhino Developer Page](https://developer.rhino3d.com/)  - Comprehensive list of Rhino for Developer Resources
- [Rhino Command Template](/commands/template_cmd.py)  -  A template file to create a Rhino Command in Python

