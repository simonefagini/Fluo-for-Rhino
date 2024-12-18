# Adding Custom Commands/Plug-ins
If you want to make your own plug-in or bundle of commands, follow the steps below.

## Adding a command in Rhino for **Windows**:

1. Run `_EditPythonScript`
2. Click **File > New**
3. Insert a name for the command and a name for the plug-in (first time only)
   
   ![](/.assets/RhinoEditPythonScriptNewCommand.png)

5. Clear the sample code and paste your own code, for instance [`template_cmd.py`](https://github.com/simonefagini/Fluo-for-Rhino/blob/main/commands/template_cmd.py)

   ![](/.assets/EditPythonScriptSampleCode.png)

6. Save
7. Relaunch Rhino
8. Run Custom Command<br>
The first time you run a Python command after starting Rhino, it may take a few extra seconds to load the Python environment. :warning:

You can then place all your future `customCommands_cmd.py` files inside of the newly created plug-in folder at: 
```plaintext
C:\Users\%username%\AppData\Roaming\McNeel\Rhinoceros\8.0\Plug-ins\PythonPlugins\CustomPlugin {12345678-abcd-1234-efgh-567890abcdef)\dev\
```
Additionally, you can set up an alias to call the command in the format:
```plaintext
alias customCommand
```

## Adding a command in Rhino for **Mac OS**:

As of December 2024, Rhino v8 on Mac OS doesn't support custom commands creation as in Rhino v8 for Windows.<br>
You can use a simple workaround and load Python scripts with an [alias](https://github.com/simonefagini/Fluo-for-Rhino/blob/main/aliases/rhinoAliases.txt).

1. Save the customCommand_cmd.py in a predefined location and add it to the `Rhino file search paths`, for instance:
```plaintext
~/Library/Application Support/McNeel/Rhinoceros/7.0/scripts/
```
2. Create an alias in the format:
```plaintext
alias ! _-RunPythonScript "customCommand_cmd.py"
```
3. Call the alias to run the script<br><br>

💡 **NOTE**: If you have a Plug-In package on your Mac - like the `Fluo-for-Rhino {df47bd45-3187-4912-8324-4b2288908bb8}` - and you place it in a `PythonPlugIns/` folder located at

```plaintext
/Users/~/Library/Application Support/McNeel/Rhinoceros/8.0/Plug-ins/
```
Rhino for Mac should still be able to load and run the custom commands.<br>
Have a look at the [official guide](https://developer.rhino3d.com/en/guides/rhinopython/7/creating-rhino-commands-using-python/) for more info.
