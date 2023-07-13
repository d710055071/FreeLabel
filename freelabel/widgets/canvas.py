from enum import Enum

from qtpy import QtWidgets
from qtpy import QtGui
from qtpy import QtCore

from label import Shape
from utils import DrawType


class DrawMode(Enum):
    DRAWING_TYPE = 0
    EDITING_TYPE = 1


CURSOR_DRAW = QtCore.Qt.CrossCursor


class Canvas(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        self.pixmap = QtGui.QPixmap()
        self.painter = QtGui.QPainter()
        self.scale = 1.0
        self.draw_model = DrawMode.EDITING_TYPE.value
        self.draw_type = DrawType.DRAW_TYPE_NONE.value
        self.currentPoint = QtCore.QPoint()
        self.current_shape = None
        self.shape_list = []
        # 窗体默认设置为不追踪。只有当鼠标按键按下时，鼠标移动时mousePressEvent才影响
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)

    # 自定义函数
    def setEditing(self, value=True):
        self.draw_model = DrawMode.EDITING_TYPE.value if value else DrawMode.DRAWING_TYPE.value

    def setDrawingType(self, value):
        self.draw_type = value

    def isDrawing(self):
        return self.draw_model == DrawMode.DRAWING_TYPE.value

    def isEditing(self):
        return self.draw_model == DrawMode.EDITING_TYPE.value

    def setPixmap(self, pixmap):
        self.pixmap = pixmap

    def setScale(self, scale):
        self.scale = scale

    def offsetToCenter(self):
        s = self.scale
        area = super(Canvas, self).size()
        w, h = self.pixmap.width() * s, self.pixmap.height() * s
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QtCore.QPointF(x, y)

    def transformPos(self, point):
        return point / self.scale - self.offsetToCenter()

    def updateStatusBar(self, point):
        pos = point
        window = self.parent().window()
        if (window.current_img_data is not None):
            self.parent().window().status_messages.setText(
                '%dx%d X: %d; Y: %d' % (self.pixmap.width(), self.pixmap.height(), pos.x(), pos.y()))

    def overrideCursor(self, cursor):
        self.restoreCursor()

        QtWidgets.QApplication.setOverrideCursor(cursor)

    def restoreCursor(self):
        QtWidgets.QApplication.restoreOverrideCursor()

    def focusOutEvent(self, ev):
        self.restoreCursor()

    def leaveEvent(self, ev):
        self.restoreCursor()
    # 系统函数

    def isInPixmap(self, pos):
        w, h = self.pixmap.width(), self.pixmap.height()
        return (0 <= pos.x() <= w - 1 and 0 <= pos.y() <= h - 1)

    def drawCrossLine(self, painter):
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.drawLine(
            0,
            int(self.currentPoint.y()),
            self.pixmap.width() - 1,
            int(self.currentPoint.y()),
        )
        painter.drawLine(
            int(self.currentPoint.x()),
            0,
            int(self.currentPoint.x()),
            self.pixmap.height() - 1,
        )

    def drawCompleted(self):
        self.current_shape.close()
        self.shape_list.append(self.current_shape)
        self.current_shape = None

    # 系统函数
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        pos = self.transformPos(event.localPos())
        self.currentPoint = pos
        # 更新状态栏信息
        self.updateStatusBar(pos)

        if self.isDrawing():
            self.overrideCursor(CURSOR_DRAW)
            if not self.current_shape:
                self.repaint()
                return
            # if self.draw_type == DrawType.DRAW_TYPE_RECT.value:

            self.repaint()
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, ev):
        pos = self.transformPos(ev.localPos())
        if ev.button() == QtCore.Qt.LeftButton:
            if self.isDrawing():
                if self.current_shape:
                    if self.draw_type == DrawType.DRAW_TYPE_POLYGON.value:
                        self.current_shape.addPoint(pos)
                        if self.current_shape.isClosed():
                            self.drawCompleted()
                    elif self.draw_type == DrawType.DRAW_TYPE_RECT.value:
                        if len(self.current_shape) == 1:
                            self.current_shape.addPoint(pos)
                            self.drawCompleted()
                        else:
                            pass
                elif self.isInPixmap(pos):
                    self.current_shape = Shape(shape_type=self.draw_type)
                    self.current_shape.addPoint(pos)
            elif self.isEditing():
                pass

    def paintEvent(self, enevt: QtGui.QPaintEvent) -> None:
        p = self.painter
        p.begin(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        p.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)

        p.scale(self.scale, self.scale)
        p.translate(self.offsetToCenter())

        p.drawPixmap(0, 0, self.pixmap)
        if (self.isDrawing() and self.currentPoint and self.isInPixmap(self.currentPoint) and self.draw_type == DrawType.DRAW_TYPE_RECT.value):
            self.drawCrossLine(p)
        # show all
        for one_shape in self.shape_list:
            one_shape.paint(p)
        # show current
        if self.current_shape is not None:
            drawing_shape = self.current_shape.copy()
            drawing_shape.addPoint(self.currentPoint)
            drawing_shape.paint(p)

        p.end()
        return super().paintEvent(enevt)
