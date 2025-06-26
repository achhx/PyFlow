from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
import numpy as np
#from PyFlow.UI.Views.VariablesWidget import default_ACNDLIST  #ACHHX Added for Variable List Record
from PyFlow.Packages.ACHHXBase.FunctionLibraries.AC_GLOBALS import AC_NDArray, isVariableOperatable


#ACHHX 定义ACAlgorithm类，继承自FunctionLibraryBase
class AC_ALGORITHM(FunctionLibraryBase):
    '''doc string for AC_ALGORITHM'''

    def __init__(self, packageName):
        super(AC_ALGORITHM, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_ADD(
        inLeft  =('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_NDArrayPin"],},),
        outArray=('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""        
        #if outArray is not None and outArray.shape == inLeft.shape and outArray.dtype == inLeft.dtype:
        isVariableOperatable(inLeft,[inRight,outArray])
        
        try:
            outArray[:] = inLeft + inRight
            result(True)
            return True
        except Exception as e:
            print(f"Error in AC_ADD: {e}")
            result(False)
            return False


    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_MINUS(
        inLeft  =('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_NDArrayPin"],},),
        outArray=('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""
        isVariableOperatable(inLeft,[inRight,outArray])
        
        try:
            outArray[:] = inLeft - inRight
            result(True)
            return True
        except Exception as e:
            print(f"Error in AC_ADD: {e}")
            result(False)
            return False


    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_MULTIPLY(
        inLeft  =('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_NDArrayPin"],},),
        outArray=('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""
        isVariableOperatable(inLeft,[inRight,outArray])
        
        try:
            outArray[:] = inLeft * inRight
            result(True)
            return True
        except Exception as e:
            print(f"Error in AC_ADD: {e}")
            result(False)
            return False

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_DIVIDE(
        inLeft  =('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inRight =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_NDArrayPin"],},),
        outArray=('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result  =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""
        isVariableOperatable(inLeft,[inRight,outArray])
        
        try:
            outArray[:] = inLeft / inRight
            result(True)
            return True
        except Exception as e:
            print(f"Error in AC_ADD: {e}")
            result(False)
            return False

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_ALGORITHM', NodeMeta.KEYWORDS: []})
    def AC_FMA(
        inLeft   =('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        inMiddle =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_NDArrayPin"],},),
        inRight  =("AnyPin",None,{PinSpecifiers.SUPPORTED_DATA_TYPES: ["FloatPin", "IntPin","AC_NDArrayPin"],},),
        outArray =('AC_NDArrayPin',None,{PinSpecifiers.CONSTRAINT: "1",}),
        result   =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""
        isVariableOperatable(inLeft,[inMiddle,inRight,outArray])
        
        try:
            outArray[:] = inLeft * inMiddle + inRight
            result(True)
            return True
        except Exception as e:
            print(f"Error in AC_ADD: {e}")
            result(False)
            return False
