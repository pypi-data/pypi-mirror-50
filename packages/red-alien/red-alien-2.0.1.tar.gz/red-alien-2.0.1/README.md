# The Red Alien Pokémon Script Compiler

This is the source repository for [Red Alien], a
compiler for the scripting system found in GBA Pokémon games.

See the [documentation] and [examples] for an overview of its
features.

[Red Alien]: http://www.cosarara.me/redalien/
[documentation]: http://www.cosarara.me/redalien/#docs
[examples]: examples/

## Running

Red Alien is built using cross-platform technologies, so it should run
everywhere. I build [windows binaries] every now and then.
Arch users can install its [AUR] package.
There is a *very* old build for Mac OSX which I don't recommend using;
run it from source instead. Same on other linux distributions or
operating systems.

[windows binaries]: http://www.cosarara.me/redalien/#windows
[AUR]: https://aur.archlinux.org/packages/red-alien-git/

Red alien is written in python and can be run directly from the
source files if you have all the dependencies installed:

Dependency | Arch package   | Debian/Ubuntu package
---------- | -------------- | ---------------------
Python 3   | `python`       | `python3`
PyQt 5     | `python-pyqt5` | `python3-pyqt5`<br>(depends on `python3`)
Python bindings for Qscintilla | `python-qscintilla-qt5` | `python3-pyqt5.qsci`<br>(depends on `python3-pyqt5`)

It can be installed system-wide (although it's not needed):

    # ./setup.py install

You can run asc-cli for CLI or asc-qt for the GUI.

If you want pks syntax highlighting in vim, you can copy utils/pks.vim to
$HOME/.vim/syntax/, and add the following line to your .vimrc:
autocmd BufRead,BufNewFile *.pks set filetype=pks

## Acknowledgements

Most of the command's information was taken from PKSV's pokedef.h (Thanks!)

The headers in stdlib/ are taken from XSE.

