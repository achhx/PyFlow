from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
import numpy as np
import ctypes
import ast
from typing import List
from typing import TypedDict
from PyFlow.Packages.ACHHXBase.FunctionLibraries.AC_GLOBALS import *


#定义AC_NDARRAY类，继承自FunctionLibraryBase
class AC_NDARRAY(FunctionLibraryBase):
    '''doc string for AC_NDARRAY'''

    def __init__(self, packageName):
        super(AC_NDARRAY, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_NDARRAY', NodeMeta.KEYWORDS: []})
    def AC_freeAllArrays(
        freeFinished=(REF,('BoolPin',None))):
        """Docstrings are in **rst** format!"""
        #global default_ACDB
        for acDataPack in default_ACDB.acDataPackList:
            acDataPack.freeArray()
        freeFinished(True)
            

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_NDARRAY', NodeMeta.KEYWORDS: []})
    def AC_defArray(
        varName=('StringPin',"ACDP_EMPTY"),
        varType=('StringPin',"double"),
        varShape=('StringPin',"[0]"),
        varState=('BoolPin',False),
        acDataPack=(REF,('AC_ArrayPin',None)),
        result=(REF,('BoolPin',False))):
        """define an ACDP variable, but not registerd!"""
        #result.enableOptions(PinOptions.RenamingEnabled)
        #global default_ACDB
        tempACDP:AC_ArrayPinStruct= AC_ArrayPinStruct.getEmpty()
        tempACDP["NDname"]  = varName
        tempACDP["NDtype"]  = varType
        tempACDP["NDshape"] = ast.literal_eval(varShape)  # 将字符串转换为列表
        tempACDP["NDstate"] = varState  # 直接使用布尔值
        acDataPack(tempACDP)  # 将数据打包到acDataPack中
        #result.createOutputPin(varName, 'StringPin', constraint=varName, structConstraint=varName, structure=StructureType.Multi)
        result(True)
        #result.rename(varName)  # 重命名输出引脚为变量名
        #isExist, index, existingPack = default_ACDB.AC_getArrayByName(varName)
        

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_NDARRAY', NodeMeta.KEYWORDS: []})
    def AC_newArray(
        inDataPackPS=('AC_ArrayPin',None),
        outDataPackPS=(REF,('AC_ArrayPin',None)),
        DBIndex=(REF,('IntPin',-1)),
        dataName=(REF,('StringPin',None)),
        dataType=(REF,('StringPin',None)),
        dataShape=(REF,('StringPin',None)),
        dataState=(REF,('BoolPin',None))):
        """Docstrings are in **rst** format!"""
        #global default_ACDB
        acdpname =inDataPackPS['NDname']
        acdptype =inDataPackPS['NDtype']
        acdpshape=inDataPackPS['NDshape']
        acdpstate=inDataPackPS['NDstate']
        acdptypeND=ACGetTypeByString(acdptype)
        acdpshapeND=np.array(acdpshape)
        isExist, index, existingPack = default_ACDB.AC_getArrayByName(acdpname)
        if isExist:
            print(f"AC_newArray: {acdpname} already exists in ACDATA_DB")
            index=index+1
        else:
            existingPack=AC_Array(acdpname,acdptypeND,acdpshapeND,acdpstate,None)
            default_ACDB.acDataPackList.append(existingPack)
            index=default_ACDB.getsizeDB()
        if acdpstate and not existingPack.getState():#如果需要分配，但是实际未分配
            existingPack.refreshArray()
        acdpstate=existingPack.getState()
        inDataPackPS['NDstate']=acdpstate
        outDataPackPS(inDataPackPS)#=(REF,('StringPin',None)),
        DBIndex(index)#=(REF,('IntPin',None)),
        dataName(acdpname)#=(REF,('StringPin',None)),
        dataType(acdptype)#=(REF,('StringPin',None)),
        dataShape(str(acdpshape))#=(REF,('StringPin',None)),
        dataState(acdpstate)#=(REF,('BoolPin',None))):
        return not isExist



    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_NDARRAY', NodeMeta.KEYWORDS: []})
    def AC_freeArray(
        inDataPack=('AC_ArrayPin',None),
        outDataPack=(REF,('AC_ArrayPin',None)),
        result    =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""
        #global default_ACDB
        acdpname  = inDataPack["NDname"]  # 获取数组名称
        acdptype  = inDataPack["NDtype"]
        acdpshape = inDataPack["NDshape"]
        acdpstate = inDataPack["NDstate"]
        isExist, index, existingPack = default_ACDB.AC_getArrayByName(acdpname)
        if isExist:
            existingPack.freeArray()
            existingPack.setState(False)  # 设置状态为False
            inDataPack["NDstate"]=False
            result(True)
            return True
        else:
            print(f"AC_freeArray: {acdpname} not found in ACDATA_DB")
            inDataPack["NDstate"]=False
            result(False)
        outDataPack(inDataPack)
        return isExist

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'AC_NDARRAY', NodeMeta.KEYWORDS: []})
    def AC_getArrayByName(
        ndname=('StringPin',"acdp_null"),
        acDataPack=(REF,('AC_ArrayPin',None))):
        """Docstrings are in **rst** format!"""
        #global default_ACDB
        isExist, index, existingPack = default_ACDB.AC_getArrayByName(ndname)
        if not isExist:
            print(f"AC_getArrayByName: {ndname} not found in ACDATA_DB")
            acDataPack(None)
            return False
        tmpACDPPS:AC_ArrayPinStruct=AC_ArrayPinStruct.getEmpty()
        tmpACDPPS['NDname']=existingPack.getName()
        tmpACDPPS['NDtype']=ACGetStringByType(existingPack.getType())
        tmpACDPPS['NDshape']=(existingPack.getShape()).tolist()
        tmpACDPPS['NDstate']=existingPack.getState()
        acDataPack(tmpACDPPS)
        print(index)
        print(existingPack.__str__())
        return True