# photo-viewer

View photos during screen idle time.


## Configuration

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


## Installation

To compile to executable, use `pyinstaller`. For example, from the command line:

```bash
python pyinstaller main.py -F --noconsole
```

where `-F` compiles to a single file, and `--noconsole` allows the program to
remain open after the launching processes exits.


# To do
* Add arguments so that the program can be run as a screensaver (*.scr)


# About

Author: Clark Steen

Started: December 2022