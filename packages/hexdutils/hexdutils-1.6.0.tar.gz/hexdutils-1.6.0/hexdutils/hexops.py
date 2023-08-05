from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from intohex import _intohex as intohex
from hextoint import _hextoint as hextoint

# +
def _hex_add(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        print("#1 arg type:", type(first), "\n#2 arg type:", type(second))
        raise TypeError("Value type must be str. Use intohex(int value)")
    result = hextoint(first) + hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)

# -
def _hex_subtract(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Value type must be str. Use intohex(int value)")
    result = hextoint(first) - hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)

# *
def _hex_multiply(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        print("#1 arg type:", type(first), "\n#2 arg type:", type(second))
        raise TypeError("Value type must be str. Use intohex(int value)")
    result = hextoint(first) * hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)

# /
def _hex_divide(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Value type must be str. Use intohex(int value)")
    result = hextoint(first) / hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)

# //
def _hex_floor(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Value type must be str. Use intohex(int value)")
    result = hextoint(first) // hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)
# %
def _hex_mod(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
        if (type(first) is not str) or (type(second) is not str):
            raise TypeError("Value type must be str. Use intohex(int value)")
        result = hextoint(first) % hextoint(second)
        if hex_output:
            return(intohex(result, hex_output_prefix, hex_output_upper))
        else:
            return(result)
# **
def _hex_power(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Value type must be str. Use intohex(int value)")
    result = hextoint(first) ** hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)
