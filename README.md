# Snazzy Walrus
_A cross-platform(hopefully) desktop image rotator._

**Do not expect this readme to always be up to date, I usually neglect updating it.**

Built with Python 3.6 (though it should theoretically work on any 3.x as long as you are not outputting non-ASCII? characters on Windows).\

Currently makes use of the following Python packages:

- Pillow (For any image processing)
- PyGObject (I think?)
- May also use PyGtk in the future (If I get around to making the GUI)


## Command Line Usage

_As this was developed for Python 3.x, users may want to specify python3 (or relevant) to make sure the scripts are run with the proper version of Python_

### Arguments
**Please be aware that any of these may be changed at any time as I try to provide better and more intuitive control of this program**

- `-l` or `--list` - specify a saved list to work with
- `-n` or `--next` - Indicate that you want to change the wallpaper immediately, and only once
- `-w` or `--wallchange` - start rotating wallpapers with specified (or implied) list
- `--interval` - specify an interval for wallpaper rotation in seconds. Default is 300, and any value below 11 will revert to the default value.
- `-u` or `--update` - Updates ImageList with new parameters, creating the list if it does not already exist. By default, this action appends images onto the list, `-o` can be specified to overwrite the list's current contents. Specifying no new options should only refresh given lists with the options initially used to create them (enabling the list to be updated with new images in the same folders)
- `-o` or `--overwrite` - Used with `-u`, specifies that user wants to overwrite the given lists with new options
- `-T` or `--terminate` or `--stop` - Tell script running the wallpaper changer (`-w`) that it should do no more and terminate itself the next time it tries to change the wallpaper. (This means it will take up to the specified interval to happen, and the wallpaper will not be changed)
- `--set-config` - Creates (if it does not exist yet) a local config file, and add the specified list to it, so that it can be used implicitly for commands like `-n` and `-w`.

**TODO: create an example or something of the following to better illustrate this functionality!**

- `-f` or `--folder` - Used when creating a list, folders to add images from. Multiple folders can be given by separating them with spaces.
- `-i` or `--include-only` - Used when creating a list, forces only using folders with the given name (and and folders within). Multiple names can be used by separating them with a space (I think).
- `-e` or `--exclude` - Used when creating a list, excludes any folders with the given names. Multiple names can be used by separating them with a space (I think).

### Example usage

Example creation of list:
`python3 /path/to/snazzywalrus/main.py -u -l /path/to/save/file.json -f /path/to/pictures -i onlyIncludeFoldersOfThisName -e excludeAnyFoldersWithThisName`

Example setting list as default list (until a new list is used at all):
`python3 /path/to/snazzywalrus/main.py --set-config -l /path/to/save/file.json`

Example switching to 'next' image with implicit saved list:
`python3 /path/to/snazzywalrus/main.py -n`

Example switching to 'next' image with explicit saved list:
`python3 /path/to/snazzywalrus/main.py -n -l /path/to/save/file.json`

Example of starting wallpaper rotation with specified (in this case 5 minute) interval and implicit list:
`python3 /path/to/snazzywalrus/main.py -w --interval 300`

Example of stopping wallpaper rotation that is running in another script (will not take effect until the next interval is reached):
`python3 /path/to/snazzywalrus/main.py -T`

## TODO

Here are some basic things that need to/I would like to be done, especially before a 1.0 release.

- Clean up argument list, and make it more intuitive.
- Create a graphical interface for creating, editing, and using lists. (Currently planning GTK, but really anything that will work cross-platform would work.)

Would be nice to have:

- Fine tuned settings/control for lists, similar to the Android version (settings objects may need more testing...)
- Better/more immediate stoppage of long-running script
 - Must only terminate a related script
 - A long-running script must be running
 - Must work across restarting computer (issues with storing pid)
- Possibly only allow 1 long-running instance at a time?
- I feel like there much more, but I cannot think of anything else right now.

## FAQ
_That nobody is asking_

**You did not following PEP8 naming conventions.**

I know and do not really care.



