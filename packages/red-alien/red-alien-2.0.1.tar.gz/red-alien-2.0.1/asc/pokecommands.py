# -*- coding: utf-8 -*-

#This file is part of ASC.

#    ASC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    ASC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with ASC.  If not, see <http://www.gnu.org/licenses/>.
# Documentation for writing this table was taken from Score_Under's
# pokedef.h

import sys
import os

def get_table_str(fn):
    # windows builds are frozen
    if getattr(sys, 'frozen', False):
        data_path = os.path.join(os.path.dirname(sys.executable), "data")
    else:
        data_path = os.path.join(os.path.dirname(__file__), "data")

    with open(os.path.join(data_path, fn), encoding="utf8") as f:
        commands_str = f.read()
    return commands_str

def dec_table(cmds):
    "Make a decompilation table from a compilation table"
    dec_pkcommands = {}

    for name, cmd in cmds.items():
        if "hex" in cmd:
            dec_pkcommands[cmd["hex"]] = name
    return dec_pkcommands

def make_tables(fn):
    pkcommands = {}
    aliases = {}
    # They will both get redefined in this exec
    #exec(get_table_str(fn))
    pkcommands, aliases, end_cmds = eval(get_table_str(fn))

    dec_pkcommands = dec_table(pkcommands)

    # Add aliases - this should be done after creating the dec table
    pkcommands_and_aliases = pkcommands.copy()
    for alias in aliases:
        normal_name = aliases[alias]
        pkcommands_and_aliases[alias] = pkcommands[normal_name]

    pkcommands = pkcommands_and_aliases
    pkcommands.update({
        "#org": {"args": ("offset", (4,))},
        "=": {"args": ("text", ("*",))},
        "#dyn": {"args": ("offset", (4,))},
        "#dynamic": {"args": ("offset", (4,))},
        "#raw": {"args": ("hex byte", (1,))},
        "if": {"args": ("comp, command, offset", (1, 1, 4))},
    })
    for key in pkcommands:
        command = pkcommands[key]
        if not 'args' in command:
            command['args'] = ("", ())
    return pkcommands, dec_pkcommands, end_cmds

pkcommands, dec_pkcommands, end_pkcommands = make_tables("commands.txt")
aicommands, dec_aicommands, end_aicommands = make_tables("aicommands.txt")
bscommands, dec_bscommands, end_bscommands = make_tables("bscommands.txt")

