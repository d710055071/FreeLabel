
import os
import cv2
from qtpy import QtWidgets
from qtpy import QtCore
from qtpy import QtGui

from qtpy.QtCore import Qt

# 自定义模块
import widgets
import utils
import qt
from enum import Enum


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # 恢复设置
        self.settings = QtCore.QSettings("dongzf", "freelabel")
        self.restore_settings()
        # 获取主菜单
        self.allActions = utils.create_struct()

        self.menu = self.create_main_menu()
        # 创建文件菜单
        self.create_file_menu()
        # 工具栏

        self.drawToolStatus = widgets.DrawType.DRAW_TYPE_NONE.value
        self.drawTool = self.createToolbar("DrawTools")
        self.create_draw_tool()

        self.current_img_data = None
        self.canvas = widgets.Canvas()

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidget(self.canvas)
        scrollArea.setWidgetResizable(True)
        self.setCentralWidget(scrollArea)
        # 最后打开的文件夹
        self.lastOpenDir = None
        # self.menuBar().addMenu("1111")
        # self.statusBar = self.statusBar()
        # self.statusBar.showMessage("显示状态栏信息",10000)

        # 定义状态栏
        self.status_messages = QtWidgets.QLabel("")
        self.statusBar().addPermanentWidget(self.status_messages)

    # 私有方法
    def restore_settings(self):
        """恢复设置"""
        # 获取设置信息
        size = self.settings.value("window/size", QtCore.QSize(600, 500))
        position = self.settings.value("window/position", QtCore.QPoint(0, 0))
        state = self.settings.value("window/state", QtCore.QByteArray())
        # 恢复设置
        self.resize(size)
        self.move(position)
        self.restoreState(state)

    def store_settings(self):
        """保存设置信息"""
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        self.settings.setValue("window/state", self.saveState())

    def create_file_menu(self):
        #
        file_menu = utils.create_struct()

        file_menu.open = qt.create_action(
            parent_widget=self,
            text=self.tr("&Open"),
            slot=self.openFile,
            tip=self.tr("Open image or label file")
        )

        file_menu.opendir = qt.create_action(
            parent_widget=self,
            text=self.tr("&Open Dir"),
            slot=self.openDir,
            icon="folder-open",
            tip=self.tr("")
        )
        file_menu.quit = qt.create_action(
            parent_widget=self,
            text=self.tr("&Quit"),
            slot=self.close,
            tip=self.tr("Quit application")
        )
        qt.add_actions(
            self.menu.file,
            (
            file_menu.open,
            file_menu.opendir,
            None,
            file_menu.quit,
            )
        )
        self.allActions.file = file_menu

    def create_edit_menu(self):
        pass

    def create_view_menu(self):
        pass

    def create_help_menu(self):
        pass

    def create_draw_tool(self):

        self.drawTool.clear()
        draw_tools = utils.create_struct()
        draw_tools.draw_point = qt.create_action(
            parent_widget=self,
            text=self.tr("Point"),
            slot=lambda: self.updateDrawToolActionStatus(widgets.DrawType.DRAW_TYPE_POINT.value),
            icon="dot",
            checkable=False,
        )
        draw_tools.draw_rect = qt.create_action(
            parent_widget=self,
            text=self.tr("Rect"),
            slot=lambda: self.updateDrawToolActionStatus(widgets.DrawType.DRAW_TYPE_RECT.value),
            icon="rect",
            checkable=False,
        )
        draw_tools.draw_polygon = qt.create_action(
            parent_widget=self,
            text=self.tr("Polygon"),
            slot=lambda: self.updateDrawToolActionStatus(widgets.DrawType.DRAW_TYPE_POLYGON.value),
            icon="polygon",
            checkable=False,
        )
        qt.add_actions(
            self.drawTool,
            (
            draw_tools.draw_point,
            draw_tools.draw_rect,
            draw_tools.draw_polygon,
            )
        )
        self.allActions.draw_tools = draw_tools

    def create_main_menu(self):
        menu = utils.create_struct(
            file=qt.create_menu(self, self.tr("&File")),
            edit=qt.create_menu(self, self.tr("&Edit")),
            view=qt.create_menu(self, self.tr("&View")),
            help=qt.create_menu(self, self.tr("&Help")),
        )
        return menu

    # 自定义函数
    def openFile(self):
        # formats = [
        #     "*.{}".format(fmt.data().decode())
        #     for fmt in QtGui.QImageReader.supportedImageFormats()
        # ]
        from PyQt5.QtWidgets import QFileDialog
        dir = QFileDialog()     # 创建文件对话框
        dir.setFileMode(QFileDialog.ExistingFiles)     # 设置多选
        dir.setDirectory(".")     # 设置初始路径为D盘
        # 设置只显示图片文件
        dir.setNameFilter("图片文件(*.jpg *.png *.bmp *.ico *.gif)")
        file_list = []
        if dir.exec_():      # 判断是否选择了文件
            file_list = dir.selectedFiles()
        if len(file_list) == 0:
            return
        image_data = cv2.imread(file_list[0])
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
        width = image_data.shape[1]
        height = image_data.shape[0]
        label_data = QtGui.QImage(image_data.data, width, height, QtGui.QImage.Format_RGB888)  # 针对RGB图显示的正确方式
        self.current_img_data = label_data
        # label_data = QtGui.QImage(image_data.data, width, height, width*3, QtGui.QImage.Format_RGB888)  # 针对RGB图显示的正确方式
        self.canvas.setPixmap(QtGui.QPixmap.fromImage(label_data))
        self.canvas.repaint()
        # TODO

    def createToolbar(self, title, actions=None):
        toolbar = widgets.ToolBar(title)
        toolbar.setObjectName("%sToolBar" % title)
        # toolbar.setOrientation(Qt.Vertical)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            utils.addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        return toolbar

    def openDir(self):

        # if self.lastOpenDir and os.path.exists(self.lastOpenDir):
        #     open_path = self.lastOpenDir
        # else:
        #     open_path = "."
        # targetDirPath = str(
        #     QtWidgets.QFileDialog.getExistingDirectory(
        #         self,
        #         self.tr("Open Directory") ,
        #         open_path,
        #         QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks,
        #     )
        # )
        # self.lastOpenDir = targetDirPath
        # file_list = utils.getCurrentFolderImages(targetDirPath)

        # image_data = cv2.imread(file_list[0])
        # image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
        # width  = image_data.shape[1]
        # height = image_data.shape[0]
        # label_data = QtGui.QImage(image_data.data, width, height, QtGui.QImage.Format_RGB888)  # 针对RGB图显示的正确方式

        # # label_data = QtGui.QImage(image_data.data, width, height, width*3, QtGui.QImage.Format_RGB888)  # 针对RGB图显示的正确方式
        # self.canvas.setPixmap(QtGui.QPixmap.fromImage(label_data))
        # self.canvas.repaint()
        a = 1

    def getDrawToolActionStatus(self, status):
        return (self.drawToolStatus & status)

    def updateDrawToolActionStatus(self, status):
        self.drawToolStatus = status
        self.canvas.setEditing(False)
        self.canvas.setDrawingType(status)
        self.allActions.draw_tools.draw_point.setEnabled(not self.getDrawToolActionStatus(widgets.DrawType.DRAW_TYPE_POINT.value))
        self.allActions.draw_tools.draw_rect.setEnabled(not self.getDrawToolActionStatus(widgets.DrawType.DRAW_TYPE_RECT.value))
        self.allActions.draw_tools.draw_polygon.setEnabled(not self.getDrawToolActionStatus(widgets.DrawType.DRAW_TYPE_POLYGON.value))

    # 系统事件
    def closeEvent(self, event):
        # 关闭时保存设置信息
        self.store_settings()
