from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from collections import namedtuple
from typing import Tuple,List,Dict
from PyFlow.Packages.ACHHXBase.FunctionLibraries.ACDATALib import ACDataPackPinStruct


class ACDataPackPin(PinBase):
    """doc string for ACDataPackPin"""
    
    def __init__(self, name, parent, direction, **kwargs):
        super(ACDataPackPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(ACDataPackPinStruct.getEmptyACDPPS())

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return 'ACDataPackPin',

    @staticmethod
    def pinDataTypeHint():
        return "ACDataPackPin",ACDataPackPinStruct.getEmptyACDPPS()

    @staticmethod
    def color():
        return (200, 200, 50, 255)

    @staticmethod
    def internalDataStructure():
        return ACDataPackPinStruct  # 返回自定义的ACDataPackPinStruct类


    @staticmethod
    def processData(data:ACDataPackPinStruct):
        if  (data            is None or     len(data) != 4):
            return ACDataPackPin.internalDataStructure()(ACDataPackPinStruct.getEmptyACDPPS())
            #return tempdata
        if  (data["NDname"]  is None or not isinstance(data["NDname"], str) )                           or \
            (data["NDtype"]  is None or not isinstance(data["NDtype"], str))                            or \
            (data["NDshape"] is None or not isinstance(data["NDshape"], list)                              \
                                     or not all(isinstance(i, int) for i in data["NDshape"]))           or \
            (data["NDstate"] is None or not isinstance(data["NDstate"], bool)):
            return ACDataPackPin.internalDataStructure()(ACDataPackPinStruct.getEmptyACDPPS())
            #return tempdata
        return ACDataPackPin.internalDataStructure()(data)
        #return data