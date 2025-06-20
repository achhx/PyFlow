from numpy import ndarray
import ctypes

def ACGetTypeByString(gettype=(str,"int")):
    tempType=ctypes.c_int
    if gettype == 'int':
        tempType=ctypes.c_int
    elif gettype == 'float':
        tempType=ctypes.c_float
    elif gettype == 'double':
        tempType=ctypes.c_double
    elif gettype == 'bool':
        tempType=ctypes.c_bool
    elif gettype == 'char':
        tempType=ctypes.c_char
    elif gettype == 'byte':
        tempType=ctypes.c_byte
    elif gettype == 'short':
        tempType=ctypes.c_short
    elif gettype == 'long':
        tempType=ctypes.c_long
    else:
        raise ValueError("Unsupported data type")
    return tempType

def ACGetStringByType(gettype=(ctypes,ctypes.c_int)):
    if gettype == ctypes.c_int:
        return 'int'
    elif gettype == ctypes.c_float:
        return 'float'
    elif gettype == ctypes.c_double:
        return 'double'
    elif gettype == ctypes.c_bool:
        return 'bool'
    elif gettype == ctypes.c_char:
        return 'char'
    elif gettype == ctypes.c_byte:
        return 'byte'
    elif gettype == ctypes.c_short:
        return 'short'
    elif gettype == ctypes.c_long:
        return 'long'
    else:
        raise ValueError("Unsupported data type")

default_ACNDLIST = []

class AC_NDArray(ndarray):
    """doc string for AC_NDArray"""
    dname = "AC_INIT_NDARRAY_NAME"  # ACHHX Added for Watch function

    def __new__(cls, shape, dtype=bool, dname="AC_INIT_NDARRAY_NAME"):
        obj = super(AC_NDArray, cls).__new__(cls, shape, dtype=dtype)
        obj.dname = dname
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.dname = getattr(obj, 'dname', "AC_INIT_NDARRAY_NAME")