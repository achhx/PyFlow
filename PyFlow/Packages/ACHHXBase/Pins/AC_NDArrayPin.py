from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from numpy import ndarray #as AC_NDArray
from PyFlow.Packages.ACHHXBase.FunctionLibraries.AC_GLOBALS import AC_NDArray  # ACHHX wapped ndarray to AC_NDArray


class AC_NDArrayPin(PinBase):
    """doc string for AC_NDArrayPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(AC_NDArrayPin, self).__init__(name, parent, direction, **kwargs)
        tmpNDarray=AC_NDArray((0), dtype=None,dname="AC_INIT_NDARRAY_NAME")
        self.setDefaultValue(tmpNDarray)
        self._isAny= True #ACHHX Added for Watch function

    @staticmethod
    def IsValuePin():
        return True
    
    @staticmethod
    def isAny(): #ACHHX Added for Watch function
        return True

    @staticmethod
    def supportedDataTypes():
        return ('AC_NDArrayPin',)

    @staticmethod
    def pinDataTypeHint():
        tmpNDarray=AC_NDArray((0), dtype=None,dname="AC_INIT_NDARRAY_NAME")  # ACHHX Added for Watch function
        return 'AC_NDArrayPin', tmpNDarray

    @staticmethod
    def color():
        return (200, 200, 50, 255)

    @staticmethod
    def internalDataStructure():
        return AC_NDArray

    @staticmethod
    def processData(data):
        if data is None:
            tmpNDarray=AC_NDArrayPin.internalDataStructure()((0), dtype=None, dname="AC_INIT_NDARRAY_NAME")  # ACHHX Added for Watch function
            return tmpNDarray
        #newData =  AC_NDArrayPin.internalDataStructure()(data.shape, dtype=data.dtype,dname=data.dname)  # ACHHX Added for Watch function
        if data.dname is None:
            data.dname = "AC_INIT_NDARRAY_NAME"
        return data
