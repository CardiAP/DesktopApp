import cv2
from PySide6.QtCore import Signal, QPointF, Qt, QRectF
from PySide6.QtGui import QImage, QPen, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QDialog, QLabel, QDialogButtonBox, QVBoxLayout

from app.models.image_selection import ImageSelection


class ImagePreview(QGraphicsView):
    cropped = Signal(QPointF, QPointF)

    def __init__(self, image_file, image_customization, image_selection):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setAlignment(Qt.AlignCenter)
        self.__click_pos, self._release_pos = image_selection.as_qt_points()
        self.__image_file = image_file
        self.__image_data = cv2.imread(str(self.__image_file.path))
        self.apply_customization(image_customization)

    def apply_customization(self, image_customization):
        self._set_image(image_customization.apply_to(self.__image_data))

    def _set_image(self, customized_image):
        qtimage = QImage(customized_image.data, customized_image.shape[1], customized_image.shape[0],
                         QImage.Format_RGB888).rgbSwapped()
        self.scene().clear()
        self._rect = QGraphicsRectItem()
        self._rect.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        self._image = self.scene().addPixmap(QPixmap.fromImage(qtimage))
        self.scene().addItem(self._rect)
        self._draw_selection()

    def mousePressEvent(self, event):
        scene_position = self.mapToScene(event.pos())
        image_position = self._image.mapFromScene(scene_position)

        if self._image.contains(image_position):
            self.__click_pos = image_position
            self._release_pos = None
        else:
            self.__click_pos = None
            self._release_pos = None

    def mouseReleaseEvent(self, event):
        scene_position = self.mapToScene(event.pos())
        image_position = self._image.mapFromScene(scene_position)

        if self._image.contains(image_position):
            self._release_pos = image_position
            if self.__click_pos is not None:
                self.cropped.emit(self.__click_pos, self._release_pos)
            else:
                self.__click_pos = None
        else:
            self.__click_pos = None
            self._release_pos = None

    def mouseMoveEvent(self, event):
        scene_position = self.mapToScene(event.pos())
        image_position = self._image.mapFromScene(scene_position)

        if (self.__click_pos is not None) and (
                self._image.contains(image_position)):
            self._rect.setRect(QRectF(self.__click_pos, scene_position))
        else:
            self._rect.setRect(QRectF())

    def _draw_selection(self):
        if (self.__click_pos is not None) and (
                self._release_pos is not None):
            self._rect.setRect(QRectF(self.__click_pos, self._release_pos))
        else:
            self._rect.setRect(QRectF())

    def image_selection(self):
        return ImageSelection.from_qt_points(self.__click_pos,
                                             self._release_pos)

    def handle_errors(self, errors):
        errors.send_details_to(self)

    def incomplete_selection(self):
        NeedToSelectImageAreaToAnalyze().exec()


class NeedToSelectImageAreaToAnalyze(QDialog):

    def __init__(self):
        super(NeedToSelectImageAreaToAnalyze, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel(
            f'Please select the section of the image you want to analyze')
        label.setWordWrap(True)
        button = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
