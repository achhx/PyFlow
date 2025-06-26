## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


import json
import os
import uuid
from inspect import getfullargspec

from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtWidgets import *

from PyFlow import GET_PACKAGES
from PyFlow import GET_PACKAGE_PATH

from PyFlow.Core.Common import *
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.Core.NodeBase import NodeBase

from PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow  import GET_PACKAGES, GET_PACKAGE_CHECKED
from inspect import getfile, getsourcefile, getsourcelines


class NodeBoxLineEdit(QLineEdit):
    def __init__(self, parent, events=True):
        super(NodeBoxLineEdit, self).__init__(parent)
        self.setParent(parent)
        self._events = events
        self.parent = parent
        self.setLocale(
            QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates)
        )
        self.setObjectName("le_nodes")
        style = (
            "border-radius: 2px;"
            + "font-size: 14px;"
            + "border-style: outset;"
            + "border-width: 1px;"
        )
        self.setStyleSheet(style)
        self.setPlaceholderText("enter node name..")


class NodeBoxTreeWidget(QTreeWidget):
    showInfo = QtCore.Signal(object)
    hideInfo = QtCore.Signal()

    def __init__(
        self,
        parent,
        canvas,
        bNodeInfoEnabled=True,
        useDragAndDrop=True,
        bGripsEnabled=True,
    ):
        super(NodeBoxTreeWidget, self).__init__(parent)
        style = (
            "border-radius: 2px;"
            + "font-size: 14px;"
            + "border-style: outset;"
            + "border-width: 1px;"
        )
        self.setStyleSheet(style)
        self.bGripsEnabled = bGripsEnabled
        self.canvas = canvas
        self.setParent(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Sunken)
        self.setObjectName("tree_nodes")
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.setColumnCount(0)
        self.setHeaderHidden(True)
        self.bUseDragAndDrop = useDragAndDrop
        if useDragAndDrop:
            self.setDragEnabled(True)
            self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setAnimated(True)
        self.categoryPaths = {}
        self.bNodeInfoEnabled = bNodeInfoEnabled
        self.currentItemChanged.connect(self.onCurrentItemChanged)
        self.suggestionsEnabled = False

    def onCurrentItemChanged(self, current, previous):
        if current is not None:
            if self.bNodeInfoEnabled:
                if not current.bCategory:
                    if current.docString is not None:
                        self.showInfo.emit(current.docString)
                else:
                    self.hideInfo.emit()

    def _isCategoryExists(self, category_name, categories):
        bFound = False
        if category_name in categories:
            return True
        if not bFound:
            for c in categories:
                sepCatNames = c.split("|")
                if len(sepCatNames) == 1:
                    if category_name == c:
                        return True
                else:
                    for i in range(0, len(sepCatNames)):
                        c = "|".join(sepCatNames)
                        if category_name == c:
                            return True
                        sepCatNames.pop()
        return False

    def insertNode(
        self,
        nodeCategoryPath,
        name,
        doc=None,
        libName=None,
        bPyNode=False,
        bCompoundNode=False,
    ):
        nodePath = nodeCategoryPath.split("|")
        categoryPath = ""
        # walk from tree top to bottom, creating folders if needed
        # also writing all paths in dict to avoid duplications
        for folderId in range(0, len(nodePath)):
            folderName = nodePath[folderId]
            if folderId == 0:
                categoryPath = folderName
                if categoryPath not in self.categoryPaths:
                    rootFolderItem = QTreeWidgetItem(self)
                    rootFolderItem.bCategory = True
                    rootFolderItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    rootFolderItem.setText(0, folderName)
                    rootFolderItem.setBackground(
                        folderId, editableStyleSheet().BgColorBright
                    )
                    self.categoryPaths[categoryPath] = rootFolderItem
            else:
                parentCategoryPath = categoryPath
                categoryPath += "|{}".format(folderName)
                if categoryPath not in self.categoryPaths:
                    childCategoryItem = QTreeWidgetItem(
                        self.categoryPaths[parentCategoryPath]
                    )
                    childCategoryItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    childCategoryItem.bCategory = True
                    childCategoryItem.setText(0, folderName)
                    childCategoryItem.setBackground(
                        0, editableStyleSheet().BgColorBright.lighter(150)
                    )
                    self.categoryPaths[categoryPath] = childCategoryItem
        # create node under constructed folder
        # TODO: Subclass QTreeWidgetItem to not create dynamic attributes. Below code is ugly
        nodeItem = QTreeWidgetItem(self.categoryPaths[categoryPath])
        nodeItem.bCategory = False
        nodeItem.bPyNode = bPyNode
        nodeItem.bCompoundNode = bCompoundNode
        nodeItem.setText(0, name)
        nodeItem.libName = libName
        nodeItem.docString = doc
        return nodeItem

    def refresh(self, pattern="", pinDirection=None, pinStructure=StructureType.Single):
        self.clear()
        self.categoryPaths = {}

        dataType = None
        if self.canvas.pressedPin is not None:
            dataType = self.canvas.pressedPin.dataType

        for package_name, package in GET_PACKAGES().items():
            # annotated functions
            for libName, lib in package.GetFunctionLibraries().items():
                foos = lib.getFunctions()
                for name, foo in foos.items():
                    foo = foo
                    libName = foo.__annotations__["lib"]
                    fooArgNames = getfullargspec(foo).args
                    fooInpTypes = set()
                    fooOutTypes = set()
                    fooInpStructs = set()
                    fooOutStructs = set()
                    if foo.__annotations__["nodeType"] == NodeTypes.Callable:
                        fooInpTypes.add("ExecPin")
                        fooOutTypes.add("ExecPin")
                        fooInpStructs.add(StructureType.Single)
                        fooOutStructs.add(StructureType.Single)

                    # consider return type if not None
                    if foo.__annotations__["return"] is not None:
                        fooOutTypes.add(foo.__annotations__["return"][0])
                        fooOutStructs.add(
                            findStructFromValue(foo.__annotations__["return"][1])
                        )

                    for index in range(len(fooArgNames)):
                        dType = foo.__annotations__[fooArgNames[index]]
                        # if tuple - this means ref pin type (output) + default value
                        # eg: (3, True) - bool with True default val
                        fooInpTypes.add(dType[0])
                        fooInpStructs.add(findStructFromValue(dType[1]))

                    nodeCategoryPath = "{0}|{1}".format(
                        package_name, foo.__annotations__["meta"][NodeMeta.CATEGORY]
                    )
                    keywords = foo.__annotations__["meta"][NodeMeta.KEYWORDS]
                    checkString = name + nodeCategoryPath + "".join(keywords)
                    if pattern.lower() in checkString.lower():
                        # create all nodes items if clicked on canvas
                        if dataType is None:
                            self.suggestionsEnabled = False
                            self.insertNode(
                                nodeCategoryPath, name, foo.__doc__, libName
                            )
                        else:
                            self.suggestionsEnabled = True
                            if pinDirection == PinDirection.Output:
                                if pinStructure != StructureType.Multi:
                                    hasMultiPins = StructureType.Multi in fooInpStructs
                                    if dataType in fooInpTypes and (
                                        pinStructure in fooInpStructs or hasMultiPins
                                    ):
                                        self.insertNode(
                                            nodeCategoryPath, name, foo.__doc__, libName
                                        )
                                elif dataType in fooInpTypes:
                                    self.insertNode(
                                        nodeCategoryPath, name, foo.__doc__, libName
                                    )
                            else:
                                if pinStructure != StructureType.Multi:
                                    hasMultiPins = StructureType.Multi in fooOutStructs
                                    if dataType in fooOutTypes and (
                                        pinStructure in fooOutStructs or hasMultiPins
                                    ):
                                        self.insertNode(
                                            nodeCategoryPath, name, foo.__doc__, libName
                                        )
                                elif dataType in fooOutTypes:
                                    self.insertNode(
                                        nodeCategoryPath, name, foo.__doc__, libName
                                    )

            # class based nodes
            for node_class in package.GetNodeClasses().values():
                if node_class.__name__ in ("setVar", "getVar"):
                    continue

                nodeCategoryPath = "{0}|{1}".format(package_name, node_class.category())

                checkString = (
                    node_class.__name__
                    + nodeCategoryPath
                    + "".join(node_class.keywords())
                )
                if pattern.lower() not in checkString.lower():
                    continue
                if dataType is None:
                    self.insertNode(
                        nodeCategoryPath, node_class.__name__, node_class.description()
                    )
                else:
                    # if pressed pin is output pin
                    # filter by nodes input types
                    hints = node_class.pinTypeHints()
                    if pinDirection == PinDirection.Output:
                        if pinStructure != StructureType.Multi:
                            hasMultiPins = StructureType.Multi in hints.inputStructs
                            if dataType in hints.inputTypes and (
                                pinStructure in hints.inputStructs or hasMultiPins
                            ):
                                self.insertNode(
                                    nodeCategoryPath,
                                    node_class.__name__,
                                    node_class.description(),
                                )
                        elif dataType in hints.inputTypes:
                            self.insertNode(
                                nodeCategoryPath,
                                node_class.__name__,
                                node_class.description(),
                            )
                    else:
                        # if pressed pin is input pin
                        # filter by nodes output types
                        if pinStructure != StructureType.Multi:
                            hasMultiPins = StructureType.Multi in hints.outputStructs
                            if dataType in hints.outputTypes and (
                                pinStructure in hints.outputStructs or hasMultiPins
                            ):
                                self.insertNode(
                                    nodeCategoryPath,
                                    node_class.__name__,
                                    node_class.description(),
                                )
                        elif dataType in hints.outputTypes:
                            self.insertNode(
                                nodeCategoryPath,
                                node_class.__name__,
                                node_class.description(),
                            )

            # populate exported py nodes
            packagePath = GET_PACKAGE_PATH(package_name)
            pyNodesRoot = os.path.join(packagePath, "PyNodes")
            if os.path.exists(pyNodesRoot):
                for path, dirs, files in os.walk(pyNodesRoot):
                    for f in files:
                        pyNodeName, extension = os.path.splitext(f)
                        if extension == ".pynode":
                            p = os.path.normpath(path)
                            folders = p.split(os.sep)
                            index = folders.index("PyNodes")
                            categorySuffix = "|".join(folders[index:])
                            category = "{0}|{1}".format(package_name, categorySuffix)
                            self.insertNode(category, pyNodeName, bPyNode=True)

            # populate exported compounds
            compoundNodesRoot = os.path.join(packagePath, "Compounds")
            if os.path.exists(compoundNodesRoot):
                for path, dirs, files in os.walk(compoundNodesRoot):
                    for f in files:
                        _, extension = os.path.splitext(f)
                        if extension == ".compound":
                            compoundsRoot = os.path.normpath(path)
                            fullCompoundPath = os.path.join(compoundsRoot, f)
                            with open(fullCompoundPath, "r") as compoundFile:
                                data = json.load(compoundFile)
                                compoundCategoryName = data["category"]
                                compoundNodeName = data["name"]
                                category = "{0}|{1}|{2}".format(
                                    package_name, "Compounds", compoundCategoryName
                                )
                                self.insertNode(
                                    category, compoundNodeName, bCompoundNode=True
                                )

            # expand all categories
            if dataType is not None:
                for categoryItem in self.categoryPaths.values():
                    categoryItem.setExpanded(True)
            self.sortItems(0, QtCore.Qt.AscendingOrder)

    def mousePressEvent(self, event):
        super(NodeBoxTreeWidget, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
                # 弹出对话框，显示“新建节点”
                item_clicked = self.currentItem()
                menu = QMenu(self)
                action_new_node = menu.addAction("New Node")
                action_new_category = menu.addAction("New Category")
                action_new_file = menu.addAction("New Library")
                # 获取全局鼠标位置并显示菜单
                cursor_pos = QtGui.QCursor.pos()
                action = menu.exec_(cursor_pos)
                if action == action_new_node:
                    packages = list(GET_PACKAGES().keys())
                    if not packages:
                        QMessageBox.information(self, "Warning", "No Available Package Found……")
                    else:
                        dlg = NewNodeDialog(packages, self)
                        if dlg.exec_() == QDialog.Accepted:
                            pkg, lib, cat, node_name = dlg.getResult()
                            if pkg and lib and cat and node_name:
                                # 1. 找到对应的Library文件路径
                                package_path = GET_PACKAGE_PATH(pkg)
                                lib_file = os.path.join(package_path, "FunctionLibraries", f"{lib}.py")
                                if not os.path.exists(lib_file):
                                    QMessageBox.information(self, "Error", f"Library file not found: {lib_file}")
                                else:
                                    # 2. 构造Node模板内容
                                    node_template = f"""
    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={{NodeMeta.CATEGORY: '{cat}', NodeMeta.KEYWORDS: []}})
    def {node_name}(
        inData=('AnyPin', None, {{}}),
        outData=(REF, ('AnyPin', None))
        ):
        \"\"\"Auto-generated node: {node_name}\"\"\"
        try:
            # TODO: implement node logic
            outData(inData)
            return True
        except Exception as e:
            print(f"Error in {node_name}: {{e}}")
            return False
"""
                                    my_line = 1 #ACHHX  记录所在文件行数
                                    content=""
                                    # 3. 检查是否已存在同名节点
                                    with open(lib_file, "r", encoding="utf-8") as f:
                                        lines = f.readlines()
                                        my_line = len(lines)     #ACHHX 获取文件总行数
                                        content = "".join(lines) #ACHHX original method f.read()
                                    if f"def {node_name}(" in content:
                                        QMessageBox.information(self, "Warning", f"Node \"{node_name}\" already exists in {lib}.py")
                                        #ACHHX 已经存在，那么文件行数就通过查找获得
                                        for idx, line in enumerate(lines, 1):
                                            if f"def {node_name}(" in line:
                                                my_line = idx
                                                break
                                    else:
                                        #ACHHX 新增节点，那么文件行数就在文件末尾
                                        my_line +=5 #ACHHX 加两行空行和两行语义描述和一行到函数名称
                                        # 4. 追加到文件末尾
                                        with open(lib_file, "a", encoding="utf-8") as f:
                                            f.write("\n" + node_template)
                                        self.parent().parent().parent().parent().parent()._clickReloadPackages() #ACHHX reload Packages to refresh new added items
                                        QMessageBox.information(self, "New Node", f"Node \"{node_name}\" is created in \"{pkg}/{lib}/{cat}\".\n")
                                    # 5. 用VSCode打开文件并定位到新节点
                                    try:
                                        # Windows下用code命令打开文件
                                        os.system("code \""+lib_file+"\":" + str(my_line)+" -r -g")
                                    except Exception as e:
                                        QMessageBox.information(self, "Error", f"Node created, but failed to open VSCode: {e}")
                            else:
                                QMessageBox.information(self, "Warning, Failed to Create New Node", f"Node \"{node_name}\" in \"{pkg}/{lib}/{cat}\".\n")
                elif action == action_new_category:
                    # 新建分类：选择Package、Library、输入Category名
                    #ACHHX TODO ???如何新建category？？？
                    packages = list(GET_PACKAGES().keys())
                    if not packages:
                        QMessageBox.information(self, "Warning", "No Available Package Found……")
                    else:
                        dlg = CategoryDialog(packages, self)
                        if dlg.exec_() == QDialog.Accepted:
                            pkg, lib, cat_name = dlg.getResult()
                            if pkg and lib and cat_name:
                                QMessageBox.information(self, "New Category", f"Category \"{cat_name}\" is created in \"{pkg}/{lib}\".\n")
                elif action == action_new_file:
                     # 通过下拉框选择已有可用的Packages
                    packages = list(GET_PACKAGES().keys())
                    if not packages:
                        QMessageBox.information(self, "Warning", "No Available Package Found……")
                    else:
                        dlg = PackageFileDialog(packages, self)
                        if dlg.exec_() == QDialog.Accepted:
                            pkg, file_name = dlg.getResult()
                            if pkg and file_name:
                                # 1. 构造目标文件路径
                                package_path = GET_PACKAGE_PATH(pkg)
                                lib_dir = os.path.join(package_path, "FunctionLibraries")
                                if not os.path.exists(lib_dir):
                                    os.makedirs(lib_dir)
                                lib_file = os.path.join(lib_dir, f"{file_name}.py")
                                # 2. 检查文件是否已存在
                                if os.path.exists(lib_file):
                                    QMessageBox.information(self, "Warning", f"Library \"{file_name}.py\" already exists in Package \"{pkg}\".")
                                else:
                                    # 3.1 创建新文件模板
                                    file_template = f"""
# {file_name}.py created by ACHHX
from PyFlow.Core.Common import *
from PyFlow.Core import IMPLEMENT_NODE
from PyFlow.Core import FunctionLibraryBase

class {file_name}(FunctionLibraryBase):
    '''Auto generated {file_name} class & category by ACHHX'''
    def __init__(self,packageName):
        super({file_name},self).__init__(packageName)
        
        
    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={{NodeMeta.CATEGORY: '{file_name}', NodeMeta.KEYWORDS: []}})
    def AC_NULLNODE(
        inData=('AnyPin', None, {{}}),
        outData=(REF, ('AnyPin', None))
        ):
        \"\"\"Auto-generated node: AC_NULLNODE\"\"\"
        # TODO: implement node logic
        outData(inData)
        return True
"""
                                    # 3. 创建新文件并写入基础模板
                                    with open(lib_file, "w", encoding="utf-8") as f:
                                        f.write("\n"+file_template)
                                    self.parent().parent().parent().parent().parent()._clickReloadPackages() #ACHHX reload Packages to refresh new added items
                                    QMessageBox.information(self, "New Library", f"Library \"{file_name}\" is created in Package \"{pkg}\".\n ")
                                    # 4. 用VSCode打开新建的文件
                                    try:
                                        os.system(f'code "{lib_file}" -r -g')
                                    except Exception as e:
                                        QMessageBox.information(self, "Error", f"Library created, but failed to open VSCode: {e}")


                            else:
                                QMessageBox.information(self, "Warning: Failed to Create New Library", f"Library \"{file_name}\" in Package \"{pkg}\".\n ")
                item_clicked = None
                return
        
        item_clicked = self.currentItem()
        if not item_clicked:
            event.ignore()
            return
        # check if clicked item is a category
        if item_clicked.bCategory:
            event.ignore()
            return
        # find top level parent
        rootItem = item_clicked
        bPyNode = False
        bCompoundNode = False
        if not item_clicked.bCategory:
            bPyNode = rootItem.bPyNode
            bCompoundNode = rootItem.bCompoundNode
        while not rootItem.parent() is None:
            rootItem = rootItem.parent()
            if not rootItem.bCategory:
                bPyNode = rootItem.bPyNode
                bCompoundNode = rootItem.bCompoundNode
        packageName = rootItem.text(0)
        pressed_text = item_clicked.text(0)
        libName = item_clicked.libName

        if pressed_text in self.categoryPaths.keys():
            event.ignore()
            return

        jsonTemplate = NodeBase.jsonTemplate()
        jsonTemplate["package"] = packageName
        jsonTemplate["lib"] = libName
        jsonTemplate["type"] = pressed_text
        jsonTemplate["name"] = pressed_text
        jsonTemplate["uuid"] = str(uuid.uuid4())
        jsonTemplate["meta"]["label"] = pressed_text
        jsonTemplate["bPyNode"] = bPyNode
        jsonTemplate["bCompoundNode"] = bCompoundNode

        if self.canvas.pressedPin is not None and self.bGripsEnabled:
            a = self.canvas.mapToScene(self.canvas.mouseReleasePos)
            jsonTemplate["x"] = a.x()
            jsonTemplate["y"] = a.y()
            node = self.canvas.createNode(jsonTemplate)
            if bPyNode or bCompoundNode:
                node.rebuild()
            self.canvas.hideNodeBox()
            pressedPin = self.canvas.pressedPin
            if pressedPin.direction == PinDirection.Input:
                for pin in node.UIoutputs.values():
                    wire = self.canvas.connectPinsInternal(pressedPin, pin)
                    if wire is not None:
                        EditorHistory().saveState("Connect pins", modify=True)
                        break
            if pressedPin.direction == PinDirection.Output:
                for pin in node.UIinputs.values():
                    wire = self.canvas.connectPinsInternal(pin, pressedPin)
                    if wire is not None:
                        EditorHistory().saveState("Connect pins", modify=True)
                        break
        else:
            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()

            pressed_text = json.dumps(jsonTemplate)
            mime_data.setText(pressed_text)
            drag.setMimeData(mime_data)
            drag.exec()

    def update(self):
        for category in self.categoryPaths.values():
            if not category.parent():
                category.setBackground(0, editableStyleSheet().BgColorBright)
            else:
                category.setBackground(
                    0, editableStyleSheet().BgColorBright.lighter(150)
                )
        #super(NodeBoxTreeWidget, self).update()

#ACHHX 创建新的节点
class NewNodeDialog(QDialog):
    """自定义对话框：选择Package、Library、Category，输入Node名称"""
    def __init__(self, packages, parent=None):
        super(NewNodeDialog, self).__init__(parent)
        self.setWindowTitle("New Node")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # 下拉框：选择Package
        self.combo_pkg = QComboBox(self)
        self.combo_pkg.addItems(packages)
        layout.addWidget(QLabel("In Package：", self))
        layout.addWidget(self.combo_pkg)

        # 下拉框：选择Library
        self.combo_lib = QComboBox(self)
        layout.addWidget(QLabel("In Library：", self))
        layout.addWidget(self.combo_lib)

        # 下拉框：选择Category
        self.combo_cat = QComboBox(self)
        layout.addWidget(QLabel("In Category：", self))
        layout.addWidget(self.combo_cat)

        # 文本框：输入Node名
        self.lineEdit = QLineEdit(self)
        layout.addWidget(QLabel("New Node Name：", self))
        layout.addWidget(self.lineEdit)

        # 按钮
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        # 初始化Library和Category下拉框
        self.updateLibraries(self.combo_pkg.currentText())
        self.combo_pkg.currentIndexChanged.connect(self.onPackageChanged)
        self.combo_lib.currentIndexChanged.connect(self.onLibraryChanged)

    def onPackageChanged(self, idx):
        pkg = self.combo_pkg.currentText()
        self.updateLibraries(pkg)

    def onLibraryChanged(self, idx):
        pkg = self.combo_pkg.currentText()
        lib = self.combo_lib.currentText()
        self.updateCategories(pkg, lib)

    def updateLibraries(self, pkg):
        self.combo_lib.clear()
        packages = GET_PACKAGES()
        libs = []
        if pkg in packages:
            libs = list(packages[pkg].GetFunctionLibraries().keys())
        self.combo_lib.addItems(libs)
        # 更新category
        if libs:
            self.updateCategories(pkg, libs[0])
        else:
            self.combo_cat.clear()

    def updateCategories(self, pkg, lib):
        self.combo_cat.clear()
        categories = set()
        packages = GET_PACKAGES()
        if pkg in packages and lib in packages[pkg].GetFunctionLibraries():
            foos = packages[pkg].GetFunctionLibraries()[lib].getFunctions()
            for foo in foos.values():
                cat = foo.__annotations__["meta"][NodeMeta.CATEGORY]
                categories.add(cat)
        self.combo_cat.addItems(sorted(categories))

    def getResult(self):
        return (self.combo_pkg.currentText(),
                self.combo_lib.currentText(),
                self.combo_cat.currentText(),
                self.lineEdit.text())
#ACHHX 创建新的分类
class CategoryDialog(QDialog):
    """自定义对话框：下拉选择Package、下拉选择Library、输入Category名"""
    def __init__(self, packages, parent=None):
        super(CategoryDialog, self).__init__(parent)
        self.setWindowTitle("New Category")
        self.setModal(True)
        self.selected_package = None
        self.selected_library = None
        self.category_name = None

        layout = QVBoxLayout(self)

        # 下拉框：选择Package
        self.combo_pkg = QComboBox(self)
        self.combo_pkg.addItems(packages)
        layout.addWidget(QLabel("In Package：", self))
        layout.addWidget(self.combo_pkg)

        # 下拉框：选择Library
        self.combo_lib = QComboBox(self)
        layout.addWidget(QLabel("In Library：", self))
        layout.addWidget(self.combo_lib)

        # 文本框：输入Category名
        self.lineEdit = QLineEdit(self)
        layout.addWidget(QLabel("New Category Name：", self))
        layout.addWidget(self.lineEdit)

        # 按钮
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        # 初始化Library下拉框
        self.updateLibraries(self.combo_pkg.currentText())
        self.combo_pkg.currentIndexChanged.connect(self.onPackageChanged)

    def onPackageChanged(self, idx):
        pkg = self.combo_pkg.currentText()
        self.updateLibraries(pkg)

    def updateLibraries(self, pkg):
        self.combo_lib.clear()
        # 获取该package下所有library
        libs = []
        packages = GET_PACKAGES()
        if pkg in packages:
            libs = list(packages[pkg].GetFunctionLibraries().keys())
        self.combo_lib.addItems(libs)

    def getResult(self):
        return self.combo_pkg.currentText(), self.combo_lib.currentText(), self.lineEdit.text()
#ACHHX 创建新的库文件
class PackageFileDialog(QDialog):
    """自定义对话框：下拉选择Package+输入文件名"""
    def __init__(self, packages, parent=None):
        super(PackageFileDialog, self).__init__(parent)
        self.setWindowTitle("New Library")
        self.setModal(True)
        self.selected_package = None
        self.file_name = None

        layout = QVBoxLayout(self)

        # 下拉框
        self.combo = QComboBox(self)
        self.combo.addItems(packages)
        layout.addWidget(QLabel("In Package：", self))
        layout.addWidget(self.combo)

        # 文本框
        self.lineEdit = QLineEdit(self)
        layout.addWidget(QLabel("New Library Name：", self))
        layout.addWidget(self.lineEdit)

        # 按钮
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def getResult(self):
        return self.combo.currentText(), self.lineEdit.text()

class NodeBoxSizeGrip(QSizeGrip):
    """docstring for NodeBoxSizeGrip."""

    def __init__(self, parent=None):
        super(NodeBoxSizeGrip, self).__init__(parent)

    def sizeHint(self):
        return QtCore.QSize(13, 13)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = event.rect()
        painter.setBrush(QtGui.QColor(80, 80, 80, 255))
        painter.drawRoundedRect(rect, 3, 3)
        painter.drawPixmap(rect, QtGui.QPixmap(":resize_diagonal.png"))
        painter.end()


class NodesBox(QFrame):
    """doc string for NodesBox"""

    def __init__(
        self,
        parent,
        canvas,
        bNodeInfoEnabled=True,
        bGripsEnabled=True,
        bUseDragAndDrop=False,
    ):
        super(NodesBox, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.bDragging = False
        self.lastCursorPos = QtCore.QPoint(0, 0)
        self.offset = QtCore.QPoint(0, 0)
        self.setMouseTracking(True)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setSpacing(1)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)
        self.splitter = QSplitter()
        self.splitter.setObjectName("nodeBoxSplitter")
        self.mainLayout.addWidget(self.splitter)
        self.bGripsEnabled = bGripsEnabled
        if self.bGripsEnabled:
            self.sizeGrip = NodeBoxSizeGrip(self)
            self.sizeGrip.setObjectName("nodeBoxSizeGrip")
            self.sizeGripLayout = QHBoxLayout()
            self.sizeGripLayout.setObjectName("sizeGripLayout")
            self.sizeGripLayout.setSpacing(1)
            self.sizeGripLayout.setContentsMargins(1, 1, 1, 1)
            spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.sizeGripLayout.addItem(spacerItem)
            self.sizeGripLayout.addWidget(self.sizeGrip)
            self.mainLayout.addLayout(self.sizeGripLayout)

        self.nodeTreeWidget = QWidget()
        self.nodeTreeWidget.setObjectName("nodeTreeWidget")
        self.nodeTreeWidget.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout(self.nodeTreeWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.splitter.addWidget(self.nodeTreeWidget)
        self.lineEdit = NodeBoxLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.lineEdit.textChanged.connect(self.leTextChanged)
        self.nodeInfoWidget = QTextBrowser()
        self.nodeInfoWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nodeInfoWidget.setObjectName("nodeBoxInfoBrowser")
        self.nodeInfoWidget.setOpenExternalLinks(True)
        self.splitter.addWidget(self.nodeInfoWidget)
        self.splitter.addWidget(self.nodeInfoWidget)
        self.nodeInfoWidget.setVisible(bNodeInfoEnabled)

        self.treeWidget = NodeBoxTreeWidget(
            self, canvas, bNodeInfoEnabled, bUseDragAndDrop, bGripsEnabled
        )
        self.treeWidget.setObjectName("nodeBoxTreeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
        self.treeWidget.refresh()

        self.treeWidget.showInfo.connect(self.onShowInfo)
        self.treeWidget.hideInfo.connect(self.onHideInfo)

    def hideEvent(self, event):
        self.bDragging = False

    def showEvent(self, event):
        self.nodeInfoWidget.setHtml("")
        self.bDragging = False

    def onShowInfo(self, restructuredText):
        self.nodeInfoWidget.show()
        self.nodeInfoWidget.setHtml(rst2html(restructuredText))

    def onHideInfo(self):
        self.nodeInfoWidget.setHtml("")

    def sizeHint(self):
        return QtCore.QSize(500, 300)

    def expandCategory(self):
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            if item.text(0) in self.treeWidget.categoryPaths:
                index = self.treeWidget.indexFromItem(item)
                self.treeWidget.expandRecursively(index)

    def leTextChanged(self):
        if self.lineEdit.text() == "":
            self.lineEdit.setPlaceholderText("enter node name..")
            self.treeWidget.refresh()
            return
        self.treeWidget.refresh(self.lineEdit.text())
        self.expandCategory()

    def mousePressEvent(self, event):
        super(NodesBox, self).mousePressEvent(event)
        if self.bGripsEnabled:
            if event.pos().y() >= self.geometry().height() - 30:
                self.bDragging = True
                self.lastCursorPos = QtGui.QCursor.pos()

    def mouseMoveEvent(self, event):
        super(NodesBox, self).mouseMoveEvent(event)
        if self.bGripsEnabled:
            if self.bDragging:
                delta = QtGui.QCursor.pos() - self.lastCursorPos
                currentPos = self.pos()
                self.move(currentPos + delta)
                self.lastCursorPos = QtGui.QCursor.pos()

    def mouseReleaseEvent(self, event):
        super(NodesBox, self).mouseReleaseEvent(event)
        self.bDragging = False
