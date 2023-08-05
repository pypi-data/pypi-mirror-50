from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from __hex_constants__ import __hex_letters, __alphabet

from intohex import _intohex as intohex

from hextoint import _hextoint as hextoint

from hexabc import _abctohex as abctohex, _hextoabc as hextoabc

from hexops import _hex_add as hex_add,\
                   _hex_subtract as hex_subtract,\
                   _hex_multiply as hex_multiply,\
                   _hex_divide as hex_divide,\
                   _hex_floor as hex_floor,\
                   _hex_mod as hex_mod,\
                   _hex_power as hex_power
