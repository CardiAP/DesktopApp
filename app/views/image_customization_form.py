from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QGridLayout, QFrame, QLabel, QSlider, \
    QLineEdit

from app.models.image_customization import ImageCustomization


class ImageCustomizationForm(QWidget):
    customization_changed = Signal(ImageCustomization)

    def __init__(self, image_customization):
        super().__init__()
        self._contrast_value = image_customization.contrast_value
        self._bright_value = image_customization.bright_value
        self._filter_diameter_value = image_customization.filter_diameter
        self._sigma_color_value = image_customization.sigma_color
        self._sigma_spatial_value = image_customization.sigma_spatial
        self._setup_form()

    def _setup_form(self):
        layout = QGridLayout()

        self._setup_bright_input(layout)
        self._setup_coontrast_input(layout)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line, 4, 0, 1, 2)

        self._setup_filter_section_title(layout)
        self._setup_filter_diameter_input(layout)
        self._setup_filter_sigma_color_input(layout)
        self._setup_filter_sigma_spatial_input(layout)

        self.setLayout(layout)

    def _setup_filter_sigma_spatial_input(self, layout):
        filter_sigma_spatial_label = QLabel(
            "Filter sigma in the coordinate space. A larger value of the parameter means that farther pixels will influence each other as long as their colors are close enough (see Sigma Color ).")
        filter_sigma_spatial_label.setWordWrap(True)
        self._filter_sigma_spatial_slider = QSlider(Qt.Horizontal)
        self._filter_sigma_spatial_slider.setMinimum(1)
        self._filter_sigma_spatial_slider.setMaximum(500)
        self._filter_sigma_spatial_slider.setValue(self._sigma_spatial_value)
        self._filter_sigma_spatial_slider.valueChanged[int].connect(
            lambda value: self._filter_sigma_spatial_changed(value))
        layout.addWidget(filter_sigma_spatial_label, 10, 0, 1, 2)
        layout.addWidget(self._filter_sigma_spatial_slider, 11, 0, 1, 2)

    def _filter_sigma_spatial_changed(self, value):
        self._sigma_spatial_value = value
        self._emit_customization_changed()

    def _setup_filter_sigma_color_input(self, layout):
        filter_sigma_color_label = QLabel(
            "Filter sigma in the color space. A larger value of the parameter means that farther colors within the pixel neighborhood will be mixed together, resulting in larger areas of semi-equal color.")
        filter_sigma_color_label.setWordWrap(True)
        self._filter_sigma_color_slider = QSlider(Qt.Horizontal)
        self._filter_sigma_color_slider.setMinimum(1)
        self._filter_sigma_color_slider.setMaximum(500)
        self._filter_sigma_color_slider.setValue(self._sigma_color_value)
        self._filter_sigma_color_slider.valueChanged[int].connect(
            lambda value: self._filter_sigma_color_changed(value))
        layout.addWidget(filter_sigma_color_label, 8, 0, 1, 2)
        layout.addWidget(self._filter_sigma_color_slider, 9, 0, 1, 2)

    def _filter_sigma_color_changed(self, value):
        self._sigma_color_value = value
        self._emit_customization_changed()

    def _setup_filter_diameter_input(self, layout):
        filter_diameter_label = QLabel(
            "Diameter of each pixel neighborhood that is used during filtering")
        filter_diameter_label.setWordWrap(True)
        self._filter_diameter_slider = QSlider(Qt.Horizontal)
        self._filter_diameter_slider.setMinimum(1)
        self._filter_diameter_slider.setMaximum(40)
        self._filter_diameter_slider.setValue(self._filter_diameter_value)
        self._filter_diameter_slider.valueChanged[int].connect(
            lambda value: self._filter_diameter_changed(value))
        layout.addWidget(filter_diameter_label, 6, 0, 1, 2)
        layout.addWidget(self._filter_diameter_slider, 7, 0, 1, 2)

    def _filter_diameter_changed(self, value):
        self._filter_diameter_value = value
        self._emit_customization_changed()

    def _setup_filter_section_title(self, layout):
        filter_title = QLabel("Bilateral filter")
        filter_title_font = QFont()
        filter_title_font.setBold(True)
        filter_title.setFont(filter_title_font)
        layout.addWidget(filter_title, 5, 0, 1, 2)

    def _setup_coontrast_input(self, layout):
        contrast_label = QLabel("Contrast (from -127 to 127)")
        self._contrast_input = QLineEdit()
        self._contrast_input.setMaxLength(4)
        self._contrast_input.setText(str(self._contrast_value))
        self._contrast_input.setDisabled(True)
        self._contrast_slider = QSlider(Qt.Horizontal, self)
        self._contrast_slider.setMinimum(-127)
        self._contrast_slider.setMaximum(127)
        self._contrast_slider.setValue(self._contrast_value)
        self._contrast_slider.valueChanged[int].connect(
            lambda value: self._contrast_changed(value))
        layout.addWidget(contrast_label, 2, 0)
        layout.addWidget(self._contrast_input, 2, 1)
        layout.addWidget(self._contrast_slider, 3, 0, 1, 2)

    def _contrast_changed(self, value):
        self._contrast_input.setText(str(value))
        self._contrast_value = value
        self._emit_customization_changed()

    def _setup_bright_input(self, layout):
        bright_label = QLabel("Bright (from -255 to 255)")
        self._bright_input = QLineEdit()
        self._bright_input.setMaxLength(4)
        self._bright_input.setText(str(self._bright_value))
        self._bright_input.setDisabled(True)
        self._bright_slider = QSlider(Qt.Horizontal, self)
        self._bright_slider.setMinimum(-255)
        self._bright_slider.setMaximum(255)
        self._bright_slider.setValue(self._bright_value)
        self._bright_slider.valueChanged[int].connect(
            lambda value: self._bright_changed(value))
        layout.addWidget(bright_label, 0, 0)
        layout.addWidget(self._bright_input, 0, 1)
        layout.addWidget(self._bright_slider, 1, 0, 1, 2)

    def _bright_changed(self, value):
        self._bright_input.setText(str(value))
        self._bright_value = value
        self._emit_customization_changed()

    def _emit_customization_changed(self):
        self.customization_changed.emit(ImageCustomization(
            self._contrast_value,
            self._bright_value,
            self._filter_diameter_value,
            self._sigma_color_value,
            self._sigma_spatial_value
        ))

    def parametrization(self):
        return ImageCustomization(
            self._contrast_value,
            self._bright_value,
            self._filter_diameter_value,
            self._sigma_color_value,
            self._sigma_spatial_value
        )

    def handle_errors(self, errors):
        errors.send_details_to(self)