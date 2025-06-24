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

class AC_NDLIST(list):
    """doc string for AC_NDLIST"""
    def __init__(self, *args, **kwargs):
        super(AC_NDLIST, self).__init__(*args, **kwargs)
        self.dname = "AC_INIT_NDLIST_NAME"  # ACHHX Added for Watch function

  #  def __array_finalize__(self, obj):
  #      if obj is None: return
  #      self.dname = getattr(obj, 'dname', "AC_INIT_NDLIST_NAME")

    def findVarsByName(self,name:str):
        """Find variables by its name in the default_ACNDLIST."""
        findVars=[]
        for array in self:
            if array._rawVariable.name == name:
                findVars.append(array)
        return findVars

    # ACHHX Added for Variable List Record, reload the append method to check for duplicates
    # and prevent adding the same variable multiple times.
    def append(self,new_array:AC_NDArray=None):
        """Append a new AC_NDArray to the append."""
        if new_array is None:
            print("Warning: Attempted to append None to default_ACNDLIST.")
            return False
        existVars = self.findVarsByName(new_array._rawVariable.name)
        if len(existVars) == 0: #ACHHX default_ACNDLIST中没有该变量，则添加到default_ACNDLIST；
            super().append(new_array)
            return True
        else :                  #ACHHX 如果default_ACNDLIST中已有该变量
            print(f"Warning: {new_array._rawVariable.name} already exists in default_ACNDLIST.")
            if len(existVars) > 1:
                raise print(f"Warning: Multiple {new_array._rawVariable.name} exists in default_ACNDLIST.")
        return False