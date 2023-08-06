#!/usr/bin/env python
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

from string import hexdigits
import sys
import os

# windows builds are frozen
if getattr(sys, 'frozen', False):
    data_path = os.path.join(os.path.dirname(sys.executable), "data")
else:
    data_path = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(data_path, "pktext.tbl"), encoding="utf8") as f:
    table_str = f.read().rstrip("\n")

def read_table_encode(table_string=table_str):
    table = table_string.split("\n")
    dictionary = {}
    for line in table:
        line_table = line.split("=")
        dictionary[line_table[1]] = int(line_table[0], 16)
    return dictionary


def read_table_decode(table_string=table_str):
    table = table_string.split("\n")
    dictionary = {}
    for line in table:
        line_table = line.split("=")
        dictionary[int(line_table[0], 16)] = line_table[1]
    return dictionary


def ascii_to_hex(astring, dictionary=read_table_encode(table_str)):
    trans_string = b''
    i = 0
    while i < len(astring):
        character = astring[i]
        if character == "\\" and astring[i + 1] in ["h", "x"]:
            if astring[i+2] in hexdigits and astring[i+3] in hexdigits:
                trans_string += bytes((int(astring[i+2:i+4], 16),))
                i += 3
        elif character in dictionary:
            trans_string += bytes((dictionary[character],))
        elif astring[i:i + 2] in dictionary:
            trans_string += bytes((dictionary[astring[i:i + 2]],))
            i += 1
        else:  # (not tested)
            #print("else")
            length = 2
            while length < 10:
                if astring[i:i + length] in dictionary:
                    trans_string += bytes((dictionary[astring[i:i + length]],))
                    i += length - 1
                    break
                else:
                    length += 1
        i += 1
    return trans_string


def hex_to_ascii(string, dictionary=read_table_decode(table_str), magic=True):
    """ string is a bytes() object """
    trans_string = ''
    for pos, byte in enumerate(string):
        # decompile color codes to \h escapes
        if magic and (pos > 0 and string[pos-1] in (0xFC, 0xFD)
                      or pos > 1 and string[pos-2] == 0xFC):
            trans_string += "\\h{:02x}".format(byte)
        elif byte in dictionary:
            trans_string += dictionary[byte]
        else:
            trans_string += "\\h{:02x}".format(byte)
    return trans_string


