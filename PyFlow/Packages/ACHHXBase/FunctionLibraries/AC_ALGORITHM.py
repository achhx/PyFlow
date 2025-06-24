from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
import numpy as np
#from PyFlow.UI.Views.VariablesWidget import default_ACNDLIST  #ACHHX Added for Variable List Record
from PyFlow.Packages.ACHHXBase.FunctionLibraries.AC_GLOBALS import AC_NDArray

#ACHHX 检查变量是否就绪（已分配空间）
@staticmethod
def isVariableReady(checkArray):
    """Check if the provided array is a valid, non-empty ndarray."""
    #ACHHX 检查变量是否为None，为None则报错
    if checkArray is None:
        raise MemoryError(f"Error: Array {checkArray} is None.")
    #ACHHX 检查变量是否是AC_NDArray,不是则直接完成检查返回True
    if not isinstance(checkArray, AC_NDArray):
        return True
    #ACHHX 检查变量是否为分配空间，为空则报错
    if checkArray.size == 0:
        raise ValueError(f"Error: Array {checkArray} is empty.")
    return True

#ACHHX 检查变量的形状是否匹配
@staticmethod
def isVariableShapeMatch(leftVar:AC_NDArray=None, rightVarList=None):
    """Check if the shapes of two variables match."""
    for rightVar in rightVarList:
        if isinstance(rightVar,AC_NDArray) and leftVar.shape != rightVar.shape:
            raise ValueError(f"Shape of {leftVar.dname} and {rightVar.dname} mismatch")
    return True

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
        isVariableReady(inLeft)
        isVariableReady(inRight)
        isVariableReady(outArray)
        isVariableShapeMatch(inLeft,[inRight,outArray])
        
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
        isVariableReady(inLeft)
        isVariableReady(inRight)
        isVariableReady(outArray)
        isVariableShapeMatch(inLeft,[inRight,outArray])
        
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
        isVariableReady(inLeft)
        isVariableReady(inRight)
        isVariableReady(outArray)
        isVariableShapeMatch(inLeft,[inRight,outArray])
        
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
        isVariableReady(inLeft)
        isVariableReady(inRight)
        isVariableReady(outArray)
        isVariableShapeMatch(inLeft,[inRight,outArray])
        
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
        isVariableReady(inLeft)
        isVariableReady(inMiddle)
        isVariableReady(inRight)
        isVariableReady(outArray)
        isVariableShapeMatch(inLeft,[inMiddle,inRight,outArray])
        
        try:
            outArray[:] = inLeft * inMiddle + inRight
            result(True)
            return True
        except Exception as e:
            print(f"Error in AC_ADD: {e}")
            result(False)
            return False




