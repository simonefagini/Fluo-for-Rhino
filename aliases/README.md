# Rhino Aliases

A custom collection of Rhino aliases aimed at improving workflow and modeling efficiency.

An __alias__ in Rhino is a _custom shorthand command_ or a _command line shortcut_ that allows users to invoke one or more chained commands.
It can be used to save time typing full commands, to quickly run complex scripts or to launch macros.

## Example format 

```plaintext

alias _Command
a1 '_Command1 _Enter
al ! _Commnad2 _Pause _Command3

```


## Import

1. Download __[`rhinoAliases.txt`](/aliases/rhinoAliases.txt)__ from the repository.
2. In Rhino go to: __Tools > Options > Aliases__
3. Click on __Import__ and select `rhinoAliases.txt` from your files


## Content

```plaintext
.
..
aliases/
├── rhinoAliases.txt 
├── updateAliases.py    
├── sortAliases.py         
└── README.md

```

- ### rhinoAliases.txt
  Main .txt file containing custom aliases

- ### updateAliases.py
  An automation tool written in .py __to offload and then re-import__ all Rhino aliases from a linked .txt file. <br>
  To reduce the need for manual updates, `updateAliases.txt`helps offload older versions of the alias list and automatically imports the newest version from a .txt file stored in a shared folder. This process makes it easier to keep aliases synchronized on different devices or among teams. 

- ### sortAliases.py
  Helping tool to __sort aliases alphabetically__.
  Rhino stores aliases in the order they are added but displays them alphabetically. <br>
  Keeps the `rhinoAliases.txt` file neatly sorted for version control, easy to manage during updates and ready for sharing.<br>
  Allows an easy check to see if a command already has an associated alias, preventing redundancy.

## Useful Links
- [Rhino Aliases](https://docs.mcneel.com/rhino/8/help/en-us/options/aliases.htm)  –  Aliases definition and default
- [Rhino Macros](https://docs.mcneel.com/rhino/8/help/en-us/information/rhinoscripting.htm)  -  Documentation on how to set a Macro and conventions
- [Naming Conventions in Rhino](https://docs.mcneel.com/rhino/8/help/en-us/information/namingconventions.htm)  –  Unicode characters and naming conventions in Rhino

## Contributing <br>
I highly value sharing knowledge as fondamental part of one's life. You take some, you give some. <br>
Feel free to adopt these aliases into your workflow and modify them to suit your preferences.<br>
Contributions are always welcome! If you have suggestions for new aliases or improvements to existing ones, don’t hesitate to reach out.<br>
Sharing is encouraged, and while it's not required, a mention or credit is always appreciated if you share or build upon this work.

---
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/simonefagini/Fluo-for-Rhino/blob/main/LICENSE)
