from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from __hex_constants__ import __hex_letters, __alphabet

import intohex
import hextoint
import hexabc
import hexops

class hexitem:
    def __init__(self, hexstr):
        self.hexstr = hexstr

    def __add__(self, other):
        if isinstance(other, hexitem):
            return hexops._hex_add(hextoint._hextoint(hexstr), hextoint._hextoint(other.hexstr), hex_output=True)
    def __sub__(self, other):
        if isinstance(other, hexitem):
            return hexops._hex_add(hextoint._hextoint(hexstr), hextoint._hextoint(other.hexstr), hex_output=True)
    def __mult__(self, other):
        if isinstance(other, hexitem):
            return hexops._hex_add(hextoint._hextoint(hexstr), hextoint._hextoint(other.hexstr), hex_output=True)
    def __truediv__(self, other):
        if isinstance(other, hexitem):
            return hexops._hex_add(hextoint._hextoint(hexstr), hextoint._hextoint(other.hexstr), hex_output=True)
    def __floordiv__(self, other):
        if isinstance(other, hexitem):
            return hexops._hex_add(hextoint._hextoint(hexstr), hextoint._hextoint(other.hexstr), hex_output=True)
    def __mod__(self, other):
        if isinstance(other, hexitem):
            return hexops._hex_add(hextoint._hextoint(hexstr), hextoint._hextoint(other.hexstr), hex_output=True)
'''
lt <
gt >
le <=
ge >=
eq ==
ne !=

isub -=
iadd +=
imul *=
idiv /=
ifloordiv //=
imod %=
ipow **=

neg -
pow +
invert ~
'''
