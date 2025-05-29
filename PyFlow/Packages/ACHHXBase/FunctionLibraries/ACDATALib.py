from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE
import numpy as np
import ctypes
import ast
from typing import List
from typing import TypedDict


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

class ACDataPackPinStruct(TypedDict):
    """doc string for ACDataPackPinStruct"""
    NDname: str
    NDtype: str
    NDshape: List[int]
    NDstate: bool
    def __init__(self, 
             NDname: str        = "ACDP_EMPTY",
             NDtype: str        = "double",
             NDshape: List[int] = [0],
             NDstate: bool      = False):
        self.NDname             = NDname
        self.NDtype             = NDtype
        self.NDshape            = NDshape
        self.NDstate            = NDstate
    
    def getEmptyACDPPS():
        tmpEmpty:ACDataPackPinStruct={"NDname": "ACDP_EMPTY",
                                      "NDtype": "double",
                                      "NDshape": [0],
                                      "NDstate": False}
        return tmpEmpty


#定义ACDataPack类，用于存储每个数组的元素
#str     DBname用于在ACDATA_DB中进行查找
#ctypes  DBtype用于记录数组的元素类型
#intList DBshape用于记录数组的形状
#bool    DBstate用于记录数组的状态
class ACDataPack:
    def __init__(self,  ndname ="ACDP_EMPTY",
                        ndtype =ctypes.c_double,
                        ndshape=[0],
                        ndstate=False,
                        ndarray=np.empty([0])):  # np.zero()  np.empty() np.array();
        self.__DPname:str        = ndname
        self.__DPtype:ctypes     = ndtype
        self.__DPshape:np.array  = ndshape
        self.__DPstate:bool      = ndstate
        self.__DParray:np.ndarray= ndarray
        if ndstate:     # 如果状态为True，则创建一个numpy数组，或者继承输入的数组
            if ndarray is None or len(ndarray) == 0: #输入数组为空或者长度为0，则重新申请空间
                self.__DParray:np.ndarray = np.zeros(ndshape, dtype=ndtype)
            else:           #输入数组不为空，则继承输入数组
                self.__DParray:np.ndarray = ndarray
        else:           # 如果状态为False，则创建一个空的numpy数组
            self.__DParray:np.ndarray= np.empty([0])  # 初始化一个空的numpy数组
        self.__DPstate=(self.__DParray.size!=0)

    def getName(self):
        return self.__DPname
    def getType(self):
        return self.__DPtype
    def getShape(self):
        return self.__DPshape
    def getState(self):
        return self.__DPstate
    def getArray(self):
        return self.__DParray
    
    def freeArray(self):
        """释放数组资源"""
        self.__DPstate = False
        if self.__DParray.size != 0:
            del self.__DParray
            self.__DParray = np.empty([0])

    def setName(self, newname):
        """设置数组名称"""
        self.__DPname = newname
    def setType(self, newtype):
        """设置数组类型"""
        self.__DPtype = newtype
        self.freeArray()
    def setShape(self, newshape):
        """设置数组形状"""
        newshape = np.array(newshape)
        self.freeArray()
    def setState(self, newstate):
        """设置数组状态"""
        self.__DPstate = newstate
        if newstate:  # 如果状态为True，则创建一个新的numpy数组
            self.__DParray = np.zeros(self.__DPshape, dtype=self.__DPtype)
        else:  # 如果状态为False，则创建一个空的numpy数组
            self.freeArray()
    def setArray(self, newarray):
        """设置数组内容"""
        if not isinstance(newarray, np.ndarray):
            raise TypeError("New array must be a numpy ndarray.")
        self.__DParray = newarray
        self.__DPstate = True
        self.__DPtype  = newarray.dtype  # 更新数组类型
        self.__DPshape = newarray.shape  # 更新数组形状
        self.__DPstate = (self.__DParray.size!=0)

    def reshapeArray(self, newshape, keepsize=True):
        """重新设置数组形状"""
        # 如果需要保持数组大小
        if keepsize:
            # 首先检查新形状是否与原形状的元素数量相同
            if np.prod(newshape) != np.prod(self.__DPshape):
                raise ValueError("New shape must have the same number of elements as the old shape.")
            # 然后检查原数组是否为空
            if self.__DParray.size == 0:
                raise ValueError("Cannot reshape an empty array.")
            # 接着检查数组大小是否与新形状匹配
            if self.__DParray.size != np.prod(newshape):
                raise ValueError("New shape must match the size of the existing array.")
            # 最后，重新设置数组形状
            self.__DParray = self.__DParray.reshape(newshape)
            self.__DPshape = np.array(newshape)  # 更新形状
            self.__DPstate = True  # 设置状态为True
        else:  # 如果不需要保持数组大小，则直接释放原来数组，根据新形状重新分配内存
            if self.__DParray.size != 0:# 如果原数组不为空，则释放原数组资源
                self.freeArray()
            self.__DParray = np.zeros(newshape, dtype=self.__DPtype)  # 创建新的数组
            self.__DPshape = np.array(newshape)  # 更新形状
            self.__DPstate = True  # 设置状态为True
        self.__DPstate = (self.__DParray.size!=0)

    def fillArray(self, value):
        """将数组内容填充为指定值"""
        if self.__DParray.size != 0:
            self.__DParray.fill(value)
        else:
            self.__DParray.fill(self.__DPshape, value)  # 如果数组为空，则创建一个新的数组并填充
        self.__DPstate = (self.__DParray.size!=0)
    
    def refreshArray(self):
        if  self.__DParray.size == 0:
            self.__DParray = np.zeros(self.__DPshape, dtype=self.__DPtype)  # 刷新数组内容
        self.__DPstate = (self.__DParray.size!=0)

    def nullifySelf(self):
        """将自身置为默认状态"""
        self.freeArray()
        self.__DPname = "ACDP_EMPTY"
        self.__DPtype = ctypes.c_double
        self.__DPshape = np.array([0])
        self.__DPstate = False
        self.__DParray = np.empty([0])

    def __str__(self):
        return f"ACDataPack(name={self.__DPname}, type={self.__DPtype}, shape={self.__DPshape}, state={self.__DPstate})"

#定义ACDATA全局列表用于存放ACDataPackPin数组资源
#元素组成包括{str=name,str=type,list=shape,NDarray,};
class ACDATA_DB:
    def __init__(self,ACDBname="ACDATA_DB"):
        self.ACDBname: str = ACDBname  # 数据库名称
        self.acDataPackList: List[ACDataPack] = []

    def getACDBName(self):
        """获取数据库名称"""
        return self.ACDBname
    
    def setACDBName(self, newname):
        """设置数据库名称"""
        self.ACDBname = newname

    def findACDataPackByName(self,acdpname):
        for i, acDataPack in enumerate(self.acDataPackList):
            if acDataPack.getName() == acdpname:
                return True,i,acDataPack
        print(f"ACDATA_DB: {acdpname} not found in ACDATA_DB")
        return False,-1,None

    def addACDataPack(self, acDataPack: ACDataPack, replaceIfExists=False):
        """添加一个ACDataPack到数据库"""
        if not isinstance(acDataPack, ACDataPack):
            raise TypeError("acDataPack must be an instance of ACDataPack.")
        isExist, index, existingPack = self.findACDataPackByName(acDataPack.getName())
        if isExist and replaceIfExists:
            print(f"ACDATA_DB: {acDataPack.getName()} already exists in ACDATA_DB, replacing it.")
            existingPack.nullifySelf()  # 释放资源
            self.acDataPackList[index] = acDataPack
            return True
        if not isExist:
            self.acDataPackList.append(acDataPack)
            return True
        print(f"ACDATA_DB: {acDataPack.getName()} already exists in ACDATA_DB, not replacing it.")
        return False

    def removeACDataPackByName(self, acdpname):
        """通过名字查找，从数据库中移除一个ACDataPack"""
        isExist, index, existingPack = self.findACDataPackByName(acdpname)
        if not isExist:
            print(f"ACDATA_DB: {acdpname} not found in ACDATA_DB")
            return False
        # 如果找到了，释放资源并删除
        else:
            existingPack.nullifySelf()
            del self.acDataPackList[index]
            return True

    def getACDataPackByName(self, acdpname):
        """通过名字查找，获取一个ACDataPack"""
        isExist, index, existingPack = self.findACDataPackByName(acdpname)
        if not isExist:
            print(f"ACDATA_DB: {acdpname} not found in ACDATA_DB")
            return None
        return existingPack
    
    def emptyACDataPackDB(self):
        """清空ACDataPack列表"""
        for acDataPack in self.acDataPackList:
            acDataPack.nullifySelf()
        self.acDataPackList.clear()  # 清空列表
    
    def __str__(self):
        """返回数据库的字符串表示"""
        return f"ACDATA_DB(name={self.ACDBname}, count={len(self.acDataPackList)})"

    def getsizeDB(self):
        return len(self.acDataPackList)

#定义ACDATA_DB的默认实例，用于默认存放数组资源
default_ACDB = ACDATA_DB(ACDBname="default_ACDB")

ACDB_List = []  # 全局列表，用于存放ACDATA_DB实例
ACDB_List.append(default_ACDB)  # 将默认实例添加到列表中

#定义ACDATALib类，继承自FunctionLibraryBase
class ACDATALib(FunctionLibraryBase):
    '''doc string for ACDATALib'''

    def __init__(self, packageName):
        super(ACDATALib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'ACDATALib', NodeMeta.KEYWORDS: []})
    def ACDATA_freeAllArrays(
        freeFinished=(REF,('BoolPin',None))):
        """Docstrings are in **rst** format!"""
        global default_ACDB
        for acDataPack in default_ACDB.acDataPackList:
            acDataPack.freeArray()
        freeFinished(True)
            

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'ACDATALib', NodeMeta.KEYWORDS: []})
    def ACDATA_defineACDPVAR(
        varName=('StringPin',"ACDP_EMPTY"),
        varType=('StringPin',"double"),
        varShape=('StringPin',"[0]"),
        varState=('BoolPin',False),
        acDataPack=(REF,('ACDataPackPin',None)),
        result=(REF,('BoolPin',False))):
        """define an ACDP variable, but not registerd!"""
        #result.enableOptions(PinOptions.RenamingEnabled)
        global default_ACDB
        tempACDP:ACDataPackPinStruct= ACDataPackPinStruct.getEmptyACDPPS()
        tempACDP["NDname"]  = varName
        tempACDP["NDtype"]  = varType
        tempACDP["NDshape"] = ast.literal_eval(varShape)  # 将字符串转换为列表
        tempACDP["NDstate"] = varState  # 直接使用布尔值
        acDataPack(tempACDP)  # 将数据打包到acDataPack中
        #result.createOutputPin(varName, 'StringPin', constraint=varName, structConstraint=varName, structure=StructureType.Multi)
        result(True)
        #result.rename(varName)  # 重命名输出引脚为变量名
        #isExist, index, existingPack = default_ACDB.findACDataPackByName(varName)
        

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'ACDATALib', NodeMeta.KEYWORDS: []})
    def ACDATA_newArray(
        inDataPackPS=('ACDataPackPin',None),
        outDataPackPS=(REF,('ACDataPackPin',None)),
        DBIndex=(REF,('IntPin',-1)),
        dataName=(REF,('StringPin',None)),
        dataType=(REF,('StringPin',None)),
        dataShape=(REF,('StringPin',None)),
        dataState=(REF,('BoolPin',None))):
        """Docstrings are in **rst** format!"""
        global default_ACDB
        acdpname =inDataPackPS['NDname']
        acdptype =inDataPackPS['NDtype']
        acdpshape=inDataPackPS['NDshape']
        acdpstate=inDataPackPS['NDstate']
        acdptypeND=ACGetTypeByString(acdptype)
        acdpshapeND=np.array(acdpshape)
        isExist, index, existingPack = default_ACDB.findACDataPackByName(acdpname)
        if isExist:
            print(f"ACDATA_newArray: {acdpname} already exists in ACDATA_DB")
            index=index+1
        else:
            existingPack=ACDataPack(acdpname,acdptypeND,acdpshapeND,acdpstate,None)
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
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'ACDATALib', NodeMeta.KEYWORDS: []})
    def ACDATA_freeArray(
        inDataPack=('ACDataPackPin',None),
        outDataPack=(REF,('ACDataPackPin',None)),
        result    =(REF,('BoolPin',None))):
        """free a specific ndarray by name!"""
        global default_ACDB
        acdpname  = inDataPack["NDname"]  # 获取数组名称
        acdptype  = inDataPack["NDtype"]
        acdpshape = inDataPack["NDshape"]
        acdpstate = inDataPack["NDstate"]
        isExist, index, existingPack = default_ACDB.findACDataPackByName(acdpname)
        if isExist:
            existingPack.freeArray()
            existingPack.setState(False)  # 设置状态为False
            inDataPack["NDstate"]=False
            result(True)
            return True
        else:
            print(f"ACDATA_freeArray: {acdpname} not found in ACDATA_DB")
            inDataPack["NDstate"]=False
            result(False)
        outDataPack(inDataPack)
        return isExist

    @staticmethod
    @IMPLEMENT_NODE(returns=None,nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'ACDATALib', NodeMeta.KEYWORDS: []})
    def ACDATA_getArrayByName(
        ndname=('StringPin',"acdp_null"),
        acDataPack=(REF,('ACDataPackPin',None))):
        """Docstrings are in **rst** format!"""
        global default_ACDB
        isExist, index, existingPack = default_ACDB.findACDataPackByName(ndname)
        if not isExist:
            print(f"ACDATA_getArrayByName: {ndname} not found in ACDATA_DB")
            acDataPack(None)
            return False
        tmpACDPPS:ACDataPackPinStruct=ACDataPackPinStruct.getEmptyACDPPS()
        tmpACDPPS['NDname']=existingPack.getName()
        tmpACDPPS['NDtype']=ACGetStringByType(existingPack.getType())
        tmpACDPPS['NDshape']=(existingPack.getShape()).tolist()
        tmpACDPPS['NDstate']=existingPack.getState()
        acDataPack(tmpACDPPS)
        print(index)
        print(existingPack.__str__())
        return True