from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
import ctypes
import ast
from typing import List
from typing import TypedDict
from PyFlow.UI.Views.VariablesWidget import default_ACNDLIST  #ACHHX Added for Variable List Record
from PyFlow.Packages.ACHHXBase.FunctionLibraries.AC_GLOBALS import AC_NDArray  # ACHHX wapped ndarray to AC_NDArray

#定义AC_NDARRAY类，继承自FunctionLibraryBase
class AC_NDARRAY(FunctionLibraryBase):
    '''doc string for AC_NDARRAY'''

    def __init__(self, packageName):
        super(AC_NDARRAY, self).__init__(packageName)


    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_NDARRAY', NodeMeta.KEYWORDS: []})
    def AC_newArray(
        inNDArray=('AC_NDArrayPin',AC_NDArray((0), dtype=None,dname="AC_INIT_NDARRAY_NAME")),  # ACHHX Added for Watch function
        outNDArray=(REF,('AC_NDArrayPin',AC_NDArray((0), dtype=None,dname="AC_INIT_NDARRAY_NAME"))),
        dataType=('StringPin',None),
        dataShape=('StringPin',None),
        result=(REF,('BoolPin',None))):
        """Allocate AC_NDArray!"""
        for varItem in default_ACNDLIST:
            if varItem._rawVariable.dataType == "AC_NDArrayPin" and \
                varItem._rawVariable.value.dname == inNDArray.dname: #varItem._rawVariable.name
                inNDArray = varItem.value
                ndtype = dataType  # 获取数据类型
                ndshape = ast.literal_eval(dataShape)  # 获取数据形状
                ndname  = inNDArray.dname
                varItem.value=AC_NDArray(ndshape,dtype=ndtype,dname=ndname)
                varItem.value.fill(0)  # 初始化为0
                outNDArray(varItem.value)
                result(True)  # 设置状态为True
                return True
        outNDArray(None)  # 如果没有找到对应的变量，返回一个空的ndarray
        result(False)  # 如果没有找到对应的变量，返回False
        return False



    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_NDARRAY', NodeMeta.KEYWORDS: []})
    def AC_freeArray(
        inNDArray=('AC_NDArrayPin',AC_NDArray((0), dtype=None,dname="AC_INIT_NDARRAY_NAME")),  # ACHHX Added for Watch function
        outNDArray=(REF,('AC_NDArrayPin',AC_NDArray((0), dtype=None,dname="AC_INIT_NDARRAY_NAME"))),  #, dname="AC_INIT_NDARRAY_NAME"
        result    =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""
        for varItem in default_ACNDLIST:
            if varItem._rawVariable.dataType == "AC_NDArrayPin" and \
                varItem._rawVariable.value.dname == inNDArray.dname: #varItem._rawVariable.name
                #del inNDArray
                #inNDArray.collect()  # 清理内存
                varItem.value=AC_NDArray([0], dtype=inNDArray.dtype,dname=inNDArray.dname)  # 初始化为0
                outNDArray(varItem.value)
                result(True)  # 设置状态为True
                return True
        outNDArray(inNDArray)
        result(False)
        return False