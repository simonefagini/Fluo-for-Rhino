# Rhino Scripts

A collection of Python-based Rhino scripts to improve my day-to-day Rhino experience.

## Content

```plaintext
.
..
scripts/
├── ..
├── blocksRenamer.py 
├── objects2sublayers.py 
├── importLayerStructure.py
├── initializeFluo4Rhino.rvb
└── README.md
```

- ### importLayerStructure.py
  A simple script to import the layer structure (name, childs, color, visible, locked) from one Rhino file to the active one. <br>
  Tested on Rhino v8 on Windows 11.

- ### objects2sublayers.py
  A script to divide multiple instances of the same named block into a user-defined number of groups, organizing them into sublayers under a user-specified parent layer. <br>
  This is especially useful for subtly varying materials or colors across groups while maintaining overall block consistency. <br>
  Tested on Rhino v8 on Windows 11.

- ### initializeFluo4Rhino.rvb
  Launched at Rhino start up via idle (_options), launches **Fluo_cmd.py** to initialize the Rhino Python Engine. <br>
  Tested on Rhino v8 on Windows 11.

- ### blocksRenamer.py
  Batch add prefix to blocks names. <br>
  Tested on Rhino v8 on Windows 11.

## Running Scripts
You can launch the command `EditPythonScript`, open your script.py and then launch it from there.
Alternatively, if you frequently use the script, you can assign it to an alias to make it faster to load.
Have a look at the [how-to.](https://github.com/simonefagini/Fluo-for-Rhino/blob/main/commands/AddingPlugins.md#adding-a-command-in-rhino-for-mac-os)




## Work in Progress

| Command Name                    | Status                       |
| ------------------------------- | ---------------------------- |
| `layerMatchProperties.py`           | :test_tube: Needs Testing  |
| `urlUpdateAliases_cmd.py`       | :test_tube: Needs Testing  |
| `objects2sublayers.py`           | 🐞 Debugging  |

 *Latest update on 14 April 2025*                      


## Useful Links
- [How to Use Scripts and Plugins](https://www.rhino3d.com/docs/guides/scripts-plugins/how-to-use/)  -  How to use scripts and plugin in Rhino
- [Rhino Developer Page](https://developer.rhino3d.com/)  - Comprehensive list of Rhino for Developer Resources

