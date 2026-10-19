from ctypes import c_double, c_int, POINTER, CDLL, c_uint8
from pathlib import Path
import numpy as np
try:
    from analysis import log
except ImportError:
    import log
try:
    from analysis import analist
except ImportError:
    import analist


class ticker:
    def __init__(self):
        self.dll = analist.loaddll().dllticker