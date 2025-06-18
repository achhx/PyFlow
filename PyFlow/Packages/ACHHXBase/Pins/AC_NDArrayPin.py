from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from numpy import ndarray as AC_ArrayND
from numpy import bool_ as ndbool


class AC_NDArrayPin(PinBase):
    """doc string for AC_NDArrayPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(AC_NDArrayPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(AC_ArrayND((0), dtype=ndbool))
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
        return 'AC_NDArrayPin', AC_ArrayND((0), dtype=ndbool)

    @staticmethod
    def color():
        return (200, 200, 50, 255)

    @staticmethod
    def internalDataStructure():
        return AC_ArrayND

    @staticmethod
    def processData(data):
        newData = AC_NDArrayPin.internalDataStructure()(data.shape, dtype=data.dtype)
        newData = data
        return newData
