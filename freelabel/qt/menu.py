
import os
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QAction 
from qtpy.QtWidgets import QMenu
from qtpy import QtGui

current_path = os.path.dirname(os.path.abspath(__file__))

def createIcon(icon):
    icon_dir = os.path.join(current_path,"../icons")
    return QtGui.QIcon(os.path.join(":/", icon_dir, "%s.svg" % icon))

def create_action(
    parent_widget : QMainWindow,
    text : str,
    slot = None,
    tip : str = "",
    icon = None,
    shortcut = None,
    checkable = False,
    enabled = True,
    checked = False,
):
    """
    创建一个动作

    Args:
        parent_widget (QMainWindow): 父窗口对象
        text (str): 显示内容
        tip (str): 提示内容
        icon (_type_, optional): 图标路径. Defaults to None.
        shortcut (_type_, optional): 快捷键. Defaults to None.
        checkable (bool, optional): 是否可以选中. Defaults to False.
        enabled (bool, optional): 可用状态. Defaults to True.
        checked (bool, optional): 选中状态. Defaults to False.
    """
    action = QAction(text,parent_widget)

    if slot is not None:
        action.triggered.connect(slot)
    
    if len(tip) > 0:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    
    if icon is not None:
        action.setIconText(text.replace(" ", "\n"))
        action.setIcon(createIcon(icon))
        pass

    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            action.setShortcuts(shortcut)
        else:
            action.setShortcut(shortcut)

    action.setCheckable(checkable)
    action.setEnabled(enabled)
    action.setChecked(checked)

    return action
def add_actions(widget,actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif isinstance(action, QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)

def create_menu(
    widget : QMainWindow ,
    title : str,
    actions = None,

):
    return widget.menuBar().addMenu(title)
