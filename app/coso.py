import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

current_dir = os.path.dirname(os.path.realpath(__file__))
point_filename = os.path.join(current_dir, "41uu2.png")


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)
        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap())
        self.pixmap_item.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def set_image(self, pixmap):
        self.pixmap_item.setPixmap(pixmap)
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)


class CropView(GraphicsView):
    resultChanged = QtCore.pyqtSignal(QtGui.QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.point_items = []

    def mousePressEvent(self, event):
        if not self.pixmap_item.pixmap().isNull():
            sp = self.mapToScene(event.pos())
            lp = self.pixmap_item.mapFromScene(sp)
            if self.pixmap_item.contains(lp):
                size = QtCore.QSize(30, 30)
                height = (
                    self.mapToScene(QtCore.QRect(QtCore.QPoint(), size))
                        .boundingRect()
                        .size()
                        .height()
                )
                pixmap = QtGui.QPixmap(point_filename)
                point_item = QtWidgets.QGraphicsPixmapItem(pixmap, self.pixmap_item)
                point_item.setOffset(
                    -QtCore.QRect(QtCore.QPoint(), pixmap.size()).center()
                )
                point_item.setPos(lp)
                scale = height
                point_item.setScale(scale)
                self.point_items.append(point_item)
                if len(self.point_items) == 4:
                    points = []
                    for it in self.point_items:
                        points.append(it.pos().toPoint())
                    self.crop(points)
                elif len(self.point_items) == 5:
                    for it in self.point_items[:-1]:
                        self.scene().removeItem(it)
                    self.point_items = [self.point_items[-1]]
            else:
                print("outside")
        super().mousePressEvent(event)

    def crop(self, points):
        # https://stackoverflow.com/a/55714969/6622587
        polygon = QtGui.QPolygonF(points)
        path = QtGui.QPainterPath()
        path.addPolygon(polygon)
        source = self.pixmap_item.pixmap()
        r = path.boundingRect().toRect().intersected(source.rect())
        pixmap = QtGui.QPixmap(source.size())
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setClipPath(path)
        painter.drawPixmap(QtCore.QPoint(), source, source.rect())
        painter.end()
        result = pixmap.copy(r)
        self.resultChanged.emit(result)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1050, 600)
        self.left_view = CropView()
        self.rigth_view = GraphicsView()
        self.left_view.resultChanged.connect(self.rigth_view.set_image)
        button = QtWidgets.QPushButton(self.tr("Browse Image"))
        button.setStyleSheet("background-color: rgb(0, 214, 157);")
        button.setFixedSize(230, 60)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.clicked.connect(self.load_image)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QGridLayout(central_widget)
        lay.addWidget(self.left_view, 0, 0)
        lay.addWidget(self.rigth_view, 0, 1)
        lay.addWidget(button, 1, 0, 1, 2, alignment=QtCore.Qt.AlignHCenter)

    @QtCore.pyqtSlot()
    def load_image(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.tif)"
        )
        if fileName:
            pixmap = QtGui.QPixmap(fileName)
            self.left_view.set_image(pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
