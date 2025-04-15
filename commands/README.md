# Rhino Commands

A collection of Python-based Rhino commands designed to enhance functionality and provide useful tools for an improved Rhino experience.

## Content

```plaintext
.
..
commands/
├── ..
├── pointPaste_cmd.py
├── whichMaterial_cmd.py
├── copyVertical_cmd.py
├── deaxo_cmd.py
├── axo_cmd.py
├── keep_cmd.py
├── centerOsnap_cmd.py
├── dupAllBorder_cmd.py
├── moveVertical_cmd.py
├── namedViewPerspective_cmd.py
├── urlUpdateAliases_cmd.py
├── obejctsByLayer_cmd.py
├── restoreView_cmd.py
├── allPointsOn_cmd.py    
├── template_cmd.py
├── AddingPlugins.md    
└── README.md
```

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
  The intended workflow starts with a selected object. <br>
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

- ### keep_cmd.py
  A command to randomly keep a user-defined percentage of pre-selected objects in Rhino, useful for quick decimation and random sampling.<br>
  Tested on Rhino v8 on Windows 11.<br>

- ### axo_cmd.py
  Python script for Rhino that deforms selected objects into axonometric projections based on customizable rotation angles.<br>
  Data is preserved as object attributes for an undestructive workflow,  with full block compatibility.<br>
  The 'deaxo' command reverts objects to their original condition.<br>

  ![](/.assets/AttributeAxoCommand.png)

   This command was inspired and made possible by this [old pdf](https://www.epfl.ch/schools/enac/atelier-maquettes/wp-content/uploads/2023/08/Creating-an-Axonometric-View-in-Rhino-1.pdf) from *EPFL Lausanne*.<br>
   If you prefer the **macro**, you can copy/paste from below.<br>

   ```plaintext
   ! _Select _Pause _SetActiveViewport Top _Rotate 0 30 _SetActiveViewport Right _Shear w0 w0,0,1 -45       _SetActiveViewport Top _Zoom _All _Extents
   ```
   Tested on Rhino v8 on Windows 11.<br>

- ### deaxo_cmd.py
  Companion command to revert axonometrically projected objects back to their original condition with a single click.<br>
  Maintains all object properties while removing projection transformations, keeping your Rhino workflow seamless and non-destructive.<br>
  Written to be used in documents where the "axo" command has previously been executed. :warning:<br>

   If you prefer the **macro**, you can copy/paste from below.<br>

   ```plaintext
   ! _Select _Pause _Right _SetActiveViewport Right _Shear w0 w0,0,1 +45 _Top _SetActiveViewport Top _Rotate 0 -30       _Perspective _SetActiveViewport Perspective _Zoom _All _Extents

   ```
   Tested on Rhino v8 on Windows 11.<br>

- ### copyVertical_cmd.py
  A command to improve the Copy Vertical workflow by preventing Project snap interference when executing the command. <br>
  The intended workflow starts with a selected object. <br>
  Tested on Rhino v8 on Windows 11.
  
- ### whichMaterial_cmd.py
  A command to check which material is applied to a selected object, or to the objects within a selected block, and return the material name for quick and easy identification.<br>
  Tested on Rhino v8 on Windows 11.

- ### pastePoint_cmd.py
  A command to paste clipboard content at a picked point in Rhino, bypassing the default behavior of pasting to original coordinates. <br>
  Assign to use with the Ctrl+Shift+V. <br>
  Tested on Rhino v8 on Windows 11.


## Work in Progress

| Command Name                    | Status                       |
| ------------------------------- | ---------------------------- |
| `pastePoint_cmd.py`           | 🧭 Beta       |
| `dupAllBorder_cmd.py`           | 🐞 Debugging  |
| `RotateRandom_cmd.py`           | :construction: In Progress  |
| `batchSwitchLayersMaterials_cmd.py`           | :bulb: Planned  |




 *Latest update on 14 Apr 2025*                      


## Useful Links
- [Creating Rhino Commands Using Python](https://developer.rhino3d.com/en/guides/rhinopython/7/creating-rhino-commands-using-python/)  -  Rhino Developers official guide on how to create Rhino commands from Python scripts
- [How to Use Scripts and Plugins](https://www.rhino3d.com/docs/guides/scripts-plugins/how-to-use/)  -  How to use scripts and plugin in Rhino
- [Rhino Developer Page](https://developer.rhino3d.com/)  - Comprehensive list of Rhino for Developer Resources
- [Rhino Command Template](/commands/template_cmd.py)  -  A template file to create a Rhino Command in Python

