# photo-viewer

Screensaver to view photos, with some additional features.


# Features

The following commands can be used:

Exit screensaver: `Esc`

Open photo: `o`

Hide photo from slideshow: `Del`

Copy photo to a favorites folder: `f`

Next/previous photo: `Right/Left`

Rotate: `Up`


# Configuration

The program requires a settings file named `photo-viewer-settings.json` with 
the following values:

`path`: list of directories in which to find photos (recursively)

`ignore_extensions`: list of file extensions to ignore

`delay_time`: time in seconds to display each photo

`hidden_directory`: name of folder in which to hide photos

`favorites`: path of Favorites directory

For example:

```json
{
    "path": ["C:/Users/Me/Pictures"],
    "ignore_extension":["ini", "mp4", "mov", "xcf"],
    "delay_time": 120,
    "hidden_directory": "Do Not Show",
    "favorites": "C:/Users/Me/Pictures/Favorites"
}
```


# Installation

To compile to executable, use `pyinstaller`. For example, from the command line:

```powershell
pyinstaller main.py -F -w
```

where `-F` compiles to a single file, and `-w` hides the console.

Next, rename the executable as `*.scr` so that it can be run as screensaver. For example:

```powershell
Move-Item .\dist\photo-viewer.exe .\dist\photo-viewer.scr -Force
Copy-Item ".\photo-viewer-settings.json" ".\dist\photo-viewer-settings.json" -Force
Copy-Item .\dist\* C:\Windows\System32\ -Force
```

# To do


# About

Author: Clark Steen

Started: December 2022