from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from __hex_constants__ import __hex_letters, __alphabet


def _hextoint(target):
    if type(target) is not str:
        raise TypeError("Argument must be str")
    decimals = []
    if target[:2] is "0x":
        target = target[2:]
    power_of_sixteen = len(target)-1
    for item in target:
        try:
            decimals.append(int(item)*(16**power_of_sixteen))
        except:
            if item.lower() in __hex_letters:
                decimals.append(__hex_letters[item.lower()]*(16**power_of_sixteen))
            else:
                raise ValueError(item, "doesn't belong to hex system")

        power_of_sixteen -= 1
    else:
        return(sum(decimals))
