


from enum import Enum

from qtpy import QtWidgets
from qtpy import QtGui
from qtpy import QtCore

class DrawType(Enum):
    DRAW_TYPE_NONE      = 0
    DRAW_TYPE_POINT     = (1 << 0)
    DRAW_TYPE_RECT      = (1 << 1)
    DRAW_TYPE_POLYGON   = (1 << 2)

class Canvas(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(Canvas,self).__init__(*args,**kwargs)
        self.__pixmap     = QtGui.QPixmap()
        self.__painter    = QtGui.QPainter()
        self.__scale      = 1.0
        self.__draw_model = DrawType.DRAW_TYPE_NONE
        
        # 窗体默认设置为不追踪。只有当鼠标按键按下时，鼠标移动时mousePressEvent才影响
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        
    # 自定义函数
    def setDrawModel(self,model):
        self.__draw_model = model
    def setPixmap(self,pixmap):
        self.__pixmap = pixmap
    def setScale(self,scale):
        self.__scale = scale
    # 私有函数
    def __offsetToCenter(self):
        s = self.__scale
        area = super(Canvas, self).size()
        w, h = self.__pixmap.width() * s, self.__pixmap.height() * s
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QtCore.QPointF(x, y)
    def __transformPos(self, point):
        return point / self.__scale - self.__offsetToCenter()
    def __updateStatusBar(self,point):
        pos = point
        window = self.parent().window()
        if not window.current_img_data == None:
            self.parent().window().status_messages.setText(
                '%dx%d X: %d; Y: %d' % (self.__pixmap.width(),self.__pixmap.height(),pos.x(), pos.y()))

    # 系统函数
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        pos = self.__transformPos(event.localPos())

        self.__updateStatusBar(pos)

        return super().mouseMoveEvent(event)
        
    def paintEvent(self, enevt: QtGui.QPaintEvent) -> None:
        
        p = self.__painter
        p.begin(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        p.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)

        p.scale(self.__scale,self.__scale)
        p.translate(self.__offsetToCenter())

        p.drawPixmap(0, 0, self.__pixmap)
        
        p.end()
        
        
        return super().paintEvent(enevt)

