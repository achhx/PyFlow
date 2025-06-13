from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
import numpy as np
from PyFlow.Packages.ACHHXBase.FunctionLibraries.AC_GLOBALS import *


#定义ACAlgorithm类，继承自FunctionLibraryBase
class AC_ALGORITHM(FunctionLibraryBase):
    '''doc string for AC_ALGORITHM'''

    def __init__(self, packageName):
        super(AC_ALGORITHM, self).__init__(packageName)


    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_ADD(
        inLeft  =('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_ArrayPin"],},),
        outArray=('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""        
        isExistL, indexL, leftDataPack  = default_ACDB.getArrayByName( inLeft["NDname"])
        leftArray  = leftDataPack.getArray()
        if type(inRight) == AC_ArrayPinStruct:
            isExistR, indexR, rightDataPack = default_ACDB.getArrayByName(inRight["NDname"])
            rightArray = rightDataPack.getArray()
        elif type(inRight) == int or type(inRight) == float:
            isExistR   = True
            rightArray = inRight
        else:
            isExistR   = False
            rightArray = None
        isExistO, indexO, outDataPack   = default_ACDB.getArrayByName(    outArray["NDname"])
        outArray   = outDataPack.getArray()
        if isExistL and isExistR and isExistO:
            outArray   = leftArray + rightArray
            result(True)
            return True
        else:
            #print(f"AC_ndarrayADD: {inLeft['NDname']，inRight['NDname']，outArray['NDname']} not found in ACDATA_DB")
            print("Array Not Found~~~")
            result(False)
            return False


    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_MINUS(
        inLeft  =('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_ArrayPin"],},),
        outArray=('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""        
        isExistL, indexL, leftDataPack  = default_ACDB.getArrayByName( inLeft["NDname"])
        leftArray  = leftDataPack.getArray()
        if type(inRight) == AC_ArrayPinStruct:
            isExistR, indexR, rightDataPack = default_ACDB.getArrayByName(inRight["NDname"])
            rightArray = rightDataPack.getArray()
        elif type(inRight) == int or type(inRight) == float:
            isExistR   = True
            rightArray = inRight
        else:
            isExistR   = False
            rightArray = None
        isExistO, indexO, outDataPack   = default_ACDB.getArrayByName(    outArray["NDname"])
        outArray   = outDataPack.getArray()
        if isExistL and isExistR and isExistO:
            outArray   = leftArray - rightArray
            result(True)
            return True
        else:
            #print(f"AC_ndarrayADD: {inLeft['NDname']，inRight['NDname']，outArray['NDname']} not found in ACDATA_DB")
            print("Array Not Found~~~")
            result(False)
            return False


    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_MULTIPLY(
        inLeft  =('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_ArrayPin"],},),
        outArray=('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""        
        isExistL, indexL, leftDataPack  = default_ACDB.getArrayByName( inLeft["NDname"])
        leftArray  = leftDataPack.getArray()
        if type(inRight) == AC_ArrayPinStruct:
            isExistR, indexR, rightDataPack = default_ACDB.getArrayByName(inRight["NDname"])
            rightArray = rightDataPack.getArray()
        elif type(inRight) == int or type(inRight) == float:
            isExistR   = True
            rightArray = inRight
        else:
            isExistR   = False
            rightArray = None
        isExistO, indexO, outDataPack   = default_ACDB.getArrayByName(    outArray["NDname"])
        outArray   = outDataPack.getArray()
        if isExistL and isExistR and isExistO:
            outArray   = leftArray * rightArray
            result(True)
            return True
        else:
            #print(f"AC_ndarrayADD: {inLeft['NDname']，inRight['NDname']，outArray['NDname']} not found in ACDATA_DB")
            print("Array Not Found~~~")
            result(False)
            return False

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_DIVIDE(
        inLeft  =('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_ArrayPin"],},),
        outArray=('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""        
        isExistL, indexL, leftDataPack  = default_ACDB.getArrayByName( inLeft["NDname"])
        leftArray  = leftDataPack.getArray()
        if type(inRight) == AC_ArrayPinStruct:
            isExistR, indexR, rightDataPack = default_ACDB.getArrayByName(inRight["NDname"])
            rightArray = rightDataPack.getArray()
        elif type(inRight) == int or type(inRight) == float:
            isExistR   = True
            rightArray = inRight
        else:
            isExistR   = False
            rightArray = None
        isExistO, indexO, outDataPack   = default_ACDB.getArrayByName(    outArray["NDname"])
        outArray   = outDataPack.getArray()
        if isExistL and isExistR and isExistO:
            outArray   = leftArray / rightArray
            result(True)
            return True
        else:
            #print(f"AC_ndarrayADD: {inLeft['NDname']，inRight['NDname']，outArray['NDname']} not found in ACDATA_DB")
            print("Array Not Found~~~")
            result(False)
            return False

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_FMA(
        inLeft   =('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inMiddle =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_ArrayPin"],},),
        inRight  =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_ArrayPin"],},),
        outArray =('AC_ArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result   =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""        
        isExistL, indexL, leftDataPack  = default_ACDB.getArrayByName( inLeft["NDname"])
        leftArray  = leftDataPack.getArray()
        if type(inMiddle) == AC_ArrayPinStruct:
            isExistM, indexM, middleDataPack = default_ACDB.getArrayByName(inMiddle["NDname"])
            middleArray = middleDataPack.getArray()
        elif type(inMiddle) == int or type(inMiddle) == float:
            isExistM    = True
            middleArray = inMiddle
        else:
            isExistM    = False
            middleArray = None
        if type(inRight) == AC_ArrayPinStruct:
            isExistR, indexR, rightDataPack = default_ACDB.getArrayByName(inRight["NDname"])
            rightArray = rightDataPack.getArray()
        elif type(inRight) == int or type(inRight) == float:
            isExistR   = True
            rightArray = inRight
        else:
            isExistR   = False
            rightArray = None
        isExistO, indexO, outDataPack   = default_ACDB.getArrayByName(    outArray["NDname"])
        outArray   = outDataPack.getArray()
        if isExistL and isExistM and isExistR and isExistO:
            outArray   = leftArray * middleArray + rightArray
            result(True)
            return True
        else:
            #print(f"AC_ndarrayADD: {inLeft['NDname']，inRight['NDname']，outArray['NDname']} not found in ACDATA_DB")
            print("Array Not Found~~~")
            result(False)
            return False




