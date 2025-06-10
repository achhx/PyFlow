from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.Packages.ACHHXBase.FunctionLibraries.AC_GLOBALS import *


class AC_ArrayPin(PinBase):
    """doc string for AC_ArrayPin"""
    
    def __init__(self, name, parent, direction, **kwargs):
        super(AC_ArrayPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(AC_ArrayPinStruct.getEmpty())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('AC_ArrayPin',)

    @staticmethod
    def pinDataTypeHint():
        return "AC_ArrayPin",AC_ArrayPinStruct.getEmpty()

    @staticmethod
    def color():
        return (200, 200, 50, 255)

    @staticmethod
    def internalDataStructure():
        return AC_ArrayPinStruct  # 返回自定义的ACDataPackPinStruct类


    @staticmethod
    def processData(data:AC_ArrayPinStruct):
        if  (data            is None or     len(data) != 4):
            return AC_ArrayPin.internalDataStructure()(AC_ArrayPinStruct.getEmpty())
            #return tempdata
        if  (data["NDname"]  is None or not isinstance(data["NDname"], str) )                           or \
            (data["NDtype"]  is None or not isinstance(data["NDtype"], str))                            or \
            (data["NDshape"] is None or not isinstance(data["NDshape"], list)                              \
                                     or not all(isinstance(i, int) for i in data["NDshape"]))           or \
            (data["NDstate"] is None or not isinstance(data["NDstate"], bool)):
            return AC_ArrayPin.internalDataStructure()(AC_ArrayPinStruct.getEmpty())
            #return tempdata
        return AC_ArrayPin.internalDataStructure()(data)
        #return data