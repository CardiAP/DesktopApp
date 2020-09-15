import os

import cv2
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF
from PyQt5.QtGui import QFont, QPixmap, QPen, QImage, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QSlider, QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QDialog, QDialogButtonBox

from app.image_settings_modal import ImageSettingsModal


class ImageSettings(QWidget):
    finished = pyqtSignal()

    def __init__(self, dyssynchrony_configuration):
        super().__init__()
        self._dyssynchrony_configuration = dyssynchrony_configuration
        self._image_path = None
        self._image_name = None
        self._image = None
        self._brigth_value = 0
        self._contrast_value = 0
        self._filter_diameter = 1
        self._sigma_color = 1
        self._sigma_spatial = 1
        self._cropping_coordinates = None

        self._setup_ui()
        self._open_next_image()
        self._reset_settings()

    def _set_customization_strategy(self):
        if self._dyssynchrony_configuration.need_to_select_customization_strategy():
            strategy = self._image_customization_stategy()
            self._dyssynchrony_configuration.set_image_customization_strategy(strategy)

    def _image_customization_stategy(self):
        modal = ImageSettingsModal()
        return modal.exec()

    def _open_next_image(self):
        self._image_path = self._dyssynchrony_configuration.next_image_path()
        self._image_name = self._dyssynchrony_configuration.current_image_name()
        self._image = cv2.imread(self._image_path)
        self._brigth_value = 0
        self._contrast_value = 0
        self._filter_diameter = 1
        self._sigma_color = 1
        self._sigma_spatial = 1
        self._cropping_coordinates = None
        self._image_cropper.set_image(self._image)

    def _setup_ui(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self._image_name_label = QLabel(f'Image: {self._image_name}', self)
        self._image_name_label.setAlignment(Qt.AlignLeft)
        self._image_name_label.setFont(font)
        self._image_name_label.setStyleSheet("max-height: 30px;")

        self._line = QFrame(self)
        self._line.setFrameShape(QFrame.HLine)
        self._line.setFrameShadow(QFrame.Sunken)

        layout = QHBoxLayout()
        widget = QWidget()
        widget.setStyleSheet("max-width: 400px;")

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)

        widget.setLayout(self._layout)
        layout.addWidget(widget)

        self._layout.addWidget(self._image_name_label)
        self._layout.addWidget(self._line)

        form_widget = QWidget(self)
        self._setup_form(form_widget)
        self._layout.addWidget(form_widget)
        self._image_cropper = ImageCropper(self)
        self._image_cropper.cropped.connect(self.set_cropping_coordinates)
        layout.addWidget(self._image_cropper)
        self.setLayout(layout)

    def _reset_settings(self):
        self._image_name_label.setText(self._image_name)
        self._bright_input.setText(str(self._brigth_value))
        self._bright_slider.setValue(self._brigth_value)
        self._contrast_input.setText(str(self._contrast_value))
        self._contrast_slider.setValue(self._contrast_value)
        self._filter_diameter_slider.setValue(self._filter_diameter)
        self._filter_sigma_color_slider.setValue(self._sigma_color)
        self._filter_sigma_spatial_slider.setValue(self._sigma_spatial)
        self._min_dist_input.setText("")
        self._calibration_input.setText("")
        self._slice_width_input.setText("0")

    def _setup_form(self, widget):
        layout = QGridLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        bright_label = QLabel("Bright (from -255 to 255)", widget)
        self._bright_input = QLineEdit(widget)
        self._bright_input.setMaxLength(4)
        self._bright_input.setText(str(self._brigth_value))
        self._bright_input.setDisabled(True)
        self._bright_slider = QSlider(Qt.Horizontal, self)
        self._bright_slider.setMinimum(-255)
        self._bright_slider.setMaximum(255)
        self._bright_slider.setValue(self._brigth_value)
        self._bright_slider.valueChanged[int].connect(self._change_brigth)

        layout.addWidget(bright_label, 0, 0)
        layout.addWidget(self._bright_input, 0, 1)
        layout.addWidget(self._bright_slider, 1, 0, 1, 2)

        contrast_label = QLabel("Contrast (from -127 to 127)", widget)
        self._contrast_input = QLineEdit(widget)
        self._contrast_input.setMaxLength(4)
        self._contrast_input.setText(str(self._contrast_value))
        self._contrast_input.setDisabled(True)
        self._contrast_slider = QSlider(Qt.Horizontal, self)
        self._contrast_slider.setMinimum(-127)
        self._contrast_slider.setMaximum(127)
        self._contrast_slider.setValue(0)
        self._contrast_slider.valueChanged[int].connect(self._change_contrast)

        layout.addWidget(contrast_label, 2, 0)
        layout.addWidget(self._contrast_input, 2, 1)
        layout.addWidget(self._contrast_slider, 3, 0, 1, 2)
        layout.addWidget(self._line, 4, 0, 1, 2)

        filter_title = QLabel("Bilateral filter", widget)
        filter_title_font = QFont()
        filter_title_font.setBold(True)
        filter_title.setFont(filter_title_font)
        layout.addWidget(filter_title, 5, 0, 1, 2)

        filter_diameter_label = QLabel("Diameter of each pixel neighborhood that is used during filtering", widget)
        filter_diameter_label.setWordWrap(True)
        self._filter_diameter_slider = QSlider(Qt.Horizontal, widget)
        self._filter_diameter_slider.setMinimum(1)
        self._filter_diameter_slider.setMaximum(40)
        self._filter_diameter_slider.setValue(1)
        self._filter_diameter_slider.valueChanged[int].connect(self._change_filter_diameter)

        layout.addWidget(filter_diameter_label, 6, 0, 1, 2)
        layout.addWidget(self._filter_diameter_slider, 7, 0, 1, 2)

        filter_sigma_color_label = QLabel(
            "Filter sigma in the color space. A larger value of the parameter means that farther colors within the pixel neighborhood will be mixed together, resulting in larger areas of semi-equal color.",
            widget)
        filter_sigma_color_label.setWordWrap(True)
        self._filter_sigma_color_slider = QSlider(Qt.Horizontal, widget)
        self._filter_sigma_color_slider.setMinimum(1)
        self._filter_sigma_color_slider.setMaximum(500)
        self._filter_sigma_color_slider.setValue(1)
        self._filter_sigma_color_slider.valueChanged[int].connect(self._change_filter_sigma_color)

        layout.addWidget(filter_sigma_color_label, 8, 0, 1, 2)
        layout.addWidget(self._filter_sigma_color_slider, 9, 0, 1, 2)

        filter_sigma_spatial_label = QLabel(
            "Filter sigma in the coordinate space. A larger value of the parameter means that farther pixels will influence each other as long as their colors are close enough (see sigmaColor ).",
            widget)
        filter_sigma_spatial_label.setWordWrap(True)
        self._filter_sigma_spatial_slider = QSlider(Qt.Horizontal, widget)
        self._filter_sigma_spatial_slider.setMinimum(1)
        self._filter_sigma_spatial_slider.setMaximum(500)
        self._filter_sigma_spatial_slider.setValue(1)
        self._filter_sigma_spatial_slider.valueChanged[int].connect(self._change_filter_sigma_spatial)

        layout.addWidget(filter_sigma_spatial_label, 10, 0, 1, 2)
        layout.addWidget(self._filter_sigma_spatial_slider, 11, 0, 1, 2)

        layout.addWidget(self._line, 12, 0, 1, 2)

        min_dist_label = QLabel("Minimum distance between peaks", widget)
        layout.addWidget(min_dist_label, 13, 0, 1, 2)

        self._min_dist_input = QLineEdit(widget)
        self._min_dist_input.setMaxLength(4)
        self._min_dist_input.setValidator(QIntValidator(widget))
        layout.addWidget(self._min_dist_input, 14, 0, 1, 2)

        self._min_dist_error = QLabel("This field is required")
        self._min_dist_error.hide()
        layout.addWidget(self._min_dist_error, 15, 0, 1, 2)

        calibration_label = QLabel("Calibration", widget)
        layout.addWidget(calibration_label, 16, 0, 1, 2)

        self._calibration_input = QLineEdit(widget)
        self._calibration_input.setMaxLength(4)
        self._calibration_input.setValidator(QIntValidator(widget))
        layout.addWidget(self._calibration_input, 17, 0, 1, 2)

        self._calibration_error = QLabel("This field is required")
        self._calibration_error.hide()
        layout.addWidget(self._calibration_error, 18, 0, 1, 2)

        slice_width_label = QLabel("The width (in pixels) of each slice", widget)
        layout.addWidget(slice_width_label, 19, 0, 1, 2)

        self._slice_width_input = QLineEdit(widget)
        self._slice_width_input.setMaxLength(4)
        self._slice_width_input.setValidator(QIntValidator(widget))
        self._slice_width_input.setText("0")
        layout.addWidget(self._slice_width_input, 20, 0, 1, 2)

        self._slice_width_error = QLabel("This field is required")
        self._slice_width_error.hide()
        layout.addWidget(self._slice_width_input, 21, 0, 1, 2)

        continue_button = QPushButton("Continue", widget)
        continue_button.clicked.connect(self._continue)
        layout.addWidget(continue_button, 22, 0, 1, 2)

        widget.setLayout(layout)

    def _form_valid(self):
        form_inputs = [
            self._min_dist_input.text(),
            self._calibration_input.text(),
            self._slice_width_input.text()
        ]
        return len([value for value in form_inputs if value == ""]) == 0

    def _validate_form(self):
        if self._min_dist_input.text() == "":
            self._min_dist_error.show()
        else:
            self._min_dist_error.hide()

        if self._calibration_input.text() == "":
            self._calibration_error.show()
        else:
            self._calibration_error.hide()

        if self._slice_width_input.text() == "":
            self._slice_width_error.show()
        else:
            self._slice_width_error.hide()

    def _continue(self):
        self._validate_form()
        if self._form_valid():
            if self._cropping_coordinates is None:
                NeedToCropImage().exec()
            else:
                self._dyssynchrony_configuration.settings_for_current_image({
                    "bright": self._brigth_value,
                    "contrast": self._contrast_value,
                    "filter_diameter": self._filter_diameter,
                    "filter_sigma_color": self._sigma_color,
                    "filter_sigma_space": self._sigma_spatial,
                    "cropping_coordinates": self._cropping_coordinates,
                    "slice_width": int(self._slice_width_input.text()),
                    "min_dist_between_maxs": int(self._min_dist_input.text()),
                    "calibration": float(self._calibration_input.text())
                })

                if self._dyssynchrony_configuration.need_to_select_customization_strategy():
                    self._set_customization_strategy()

                if self._dyssynchrony_configuration.are_there_more_images():
                    self._open_next_image()
                    self._reset_settings()
                else:
                    self.finished.emit()

    def _change_filter_diameter(self, filter_diameter):
        self._filter_diameter = filter_diameter
        self._update_image()

    def _change_filter_sigma_color(self, sigma_color):
        self._sigma_color = sigma_color
        self._update_image()

    def _change_filter_sigma_spatial(self, sigma_spatial):
        self._sigma_spatial = sigma_spatial
        self._update_image()

    def _change_contrast(self, contrast):
        self._contrast_value = contrast
        self._contrast_input.setText(str(contrast))
        self._update_image()

    def _change_brigth(self, brightness):
        self._brigth_value = brightness
        self._bright_input.setText(str(brightness))
        self._update_image()

    def _update_image(self):
        alpha_contrast = float(131 * (self._contrast_value + 127)) / (127 * (131 - self._contrast_value))
        gamma_contrast = 127 * (1 - alpha_contrast)

        if self._brigth_value > 0:
            shadow = self._brigth_value
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + self._brigth_value

        alpha_brightness = (highlight - shadow) / 255
        gamma_brightness = shadow

        image = self._image
        image = cv2.addWeighted(image, alpha_brightness, image, 0, gamma_brightness)
        image = cv2.addWeighted(image, alpha_contrast, image, 0, gamma_contrast)
        image = cv2.bilateralFilter(image, self._filter_diameter, self._sigma_color, self._sigma_spatial)
        self._image_cropper.set_image(image)

    def set_cropping_coordinates(self, position1, position2):
        self._cropping_coordinates = {
            "x_start": min(position1.x(), position2.x()),
            "y_start": min(position1.y(), position2.y()),
            "x_end": max(position1.x(), position2.x()),
            "y_end": max(position1.y(), position2.y())
        }

    def _get_image_path(self):
        path = self._form_data["path"]

        if os.path.isfile(path):
            return path
        else:
            return [f'{path}/{file}' for file in os.listdir(path) if file.endswith(".tif")][0]


class ImageCropper(QGraphicsView):
    cropped = pyqtSignal(QPointF, QPointF)

    def __init__(self, parent=None, ):
        super().__init__(QGraphicsScene(), parent)
        self.setAlignment(Qt.AlignCenter)
        self._click_pos = None
        self._release_pos = None

    def set_image(self, image):
        qtimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.scene().clear()
        self._rect = QGraphicsRectItem()
        self._rect.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        self._image = self.scene().addPixmap(QPixmap.fromImage(qtimage))
        self.scene().addItem(self._rect)

    def mousePressEvent(self, event):
        scene_position = self.mapToScene(event.pos())
        image_position = self._image.mapFromScene(scene_position)

        if self._image.contains(image_position):
            self._click_pos = image_position
            self._release_pos = None
        else:
            self._click_pos = None
            self._release_pos = None

    def mouseReleaseEvent(self, event):
        scene_position = self.mapToScene(event.pos())
        image_position = self._image.mapFromScene(scene_position)

        if self._image.contains(image_position):
            self._release_pos = image_position
            if self._click_pos is not None:
                self.cropped.emit(self._click_pos, self._release_pos)
            else:
                self._click_pos = None
        else:
            self._click_pos = None
            self._release_pos = None

    def mouseMoveEvent(self, event):
        scene_position = self.mapToScene(event.pos())
        image_position = self._image.mapFromScene(scene_position)

        if (self._click_pos is not None) and (self._image.contains(image_position)):
            self._rect.setRect(QRectF(self._click_pos, scene_position))
        else:
            self._rect.setRect(QRectF())


class NeedToCropImage(QDialog):

    def __init__(self):
        super(NeedToCropImage, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel(f'Please select the section of the image you want to analyze')
        label.setWordWrap(True)
        button = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
