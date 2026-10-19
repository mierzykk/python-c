from ctypes import c_double, c_int, POINTER, CDLL, c_uint8
from pathlib import Path
import numpy as np

dll = None
class loaddll:
    def __init__(self):
        self.dlldf = CDLL(str((Path(__file__).parent/ ".." / "native" / "df.dll").resolve()))
        self.dllticker = CDLL(str((Path(__file__).parent/ ".." / "native" / "ticker.dll").resolve()))