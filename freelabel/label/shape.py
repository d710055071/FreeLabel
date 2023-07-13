import copy
from qtpy import QtGui
from qtpy import QtCore
from utils import DrawType


class Shape(object):
    point_size = 8
    scale = 1.0

    def __init__(self, label=None, shape_type=None):
        self.point_list = []
        self.shape_type = shape_type
        self.closed = False

    def addPoint(self, point):
        if self.point_list and point == self.point_list[0]:
            self.close()
        else:
            self.point_list.append(point)

    def getRect(self, pt1, pt2):
        x1, y1 = pt1.x(), pt1.y()
        x2, y2 = pt2.x(), pt2.y()
        return QtCore.QRectF(x1, y1, x2 - x1, y2 - y1)

    def drawVertex(self, path, i):
        d = self.point_size / self.scale
        point = self.point_list[i]
        path.addEllipse(point, d / 2.0, d / 2.0)

    def isClosed(self):
        return self.closed

    def close(self):
        self.closed = True

    def paint(self, painter):
        if self.point_list:
            color = QtGui.QColor(255, 255, 255)
            pen = QtGui.QPen(color)
            pen.setWidth(1)
            painter.setPen(pen)
            line_path = QtGui.QPainterPath()
            vrtx_path = QtGui.QPainterPath()
        if self.shape_type == DrawType.DRAW_TYPE_RECT.value:
            if len(self.point_list) == 2:
                line_path.addRect(self.getRect(*self.point_list))
                for i in range(len(self.point_list)):
                    self.drawVertex(vrtx_path, i)
        else:
            line_path.moveTo(self.point_list[0])
            for i, p in enumerate(self.point_list):
                line_path.lineTo(p)
                self.drawVertex(vrtx_path, i)
            if self.isClosed():
                line_path.lineTo(self.point_list[0])
        painter.drawPath(line_path)
        painter.drawPath(vrtx_path)
        painter.fillPath(vrtx_path, QtGui.QColor(0, 0, 255))
        # painter.fillPath(line_path, color)

    def copy(self):
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.point_list)

    def __getitem__(self, key):
        return self.point_list[key]

    def __setitem__(self, key, value):
        self.point_list[key] = value
