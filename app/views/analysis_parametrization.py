import os

import cv2
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, \
    QSlider, QGridLayout, QLineEdit, QHBoxLayout, QPushButton

from app.image_settings_modal import ImageSettingsModal
from app.views.analysis_input_parameters_form import \
    AnalysisInputParametersForm
from app.views.image_customization_form import ImageCustomizationForm
from app.views.image_preview import ImagePreview, \
    NeedToSelectImageAreaToAnalyze


class AnalysisParametrizationErrors(object):
    def __init__(self, image_selection_errors, input_parameters_errors,
                 image_customization_errors):
        self._image_customization_errors = image_customization_errors
        self._input_parameters_errors = input_parameters_errors
        self._image_selection_errors = image_selection_errors

    def any(self):
        return self._image_selection_errors.any() or \
               self._input_parameters_errors.any() or \
               self._image_customization_errors.any()

    def for_image_customization_form(self):
        return self._image_customization_errors

    def for_analysis_input_form(self):
        return self._input_parameters_errors

    def for_image_preview(self):
        return self._image_selection_errors


class AnalysisParametrization2(object):
    def __init__(self, file, image_customization, input_parameters,
                 image_selection):
        self._file = file
        self._image_selection = image_selection
        self._input_parameters = input_parameters
        self._image_customization = image_customization

    def validate(self):
        return AnalysisParametrizationErrors(self._image_selection.validate(),
                                             self._input_parameters.validate(),
                                             self._image_customization.validate())

    def copy_for(self, file):
        return self.__class__(file, self._image_customization.copy(),
                              self._input_parameters.copy(),
                              self._image_customization.copy())


class ParametersCustomizationStrategy(object):
    SINGLE_IMAGE_CUSTOMIZATION_STRATEGY = 1
    MULTIPLE_IMAGE_CUSTOMIZATION_STRATEGY = 0

    def __init__(self, strategy_id):
        self._strategy_id = strategy_id

    def apply_to(self, analysis, parametrization):
        if self.use_same_parametrization_for_all():
            analysis.use_same_parametrization_for_all(parametrization)
        elif self.use_different_parametrization_for_each():
            analysis.use_different_parametrization_for_each(parametrization)

    def use_same_parametrization_for_all(self):
        return self.SINGLE_IMAGE_CUSTOMIZATION_STRATEGY == self._strategy_id

    def use_different_parametrization_for_each(self):
        return self.MULTIPLE_IMAGE_CUSTOMIZATION_STRATEGY == self._strategy_id


class AnalysisParametrizationForm(QWidget):
    analysis_parametrization_finished = pyqtSignal(AnalysisParametrization2)
    go_back = pyqtSignal()

    def __init__(self, file):
        super().__init__()
        self._file = file
        self._setup()

    def _setup(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        self._line = QFrame(self)
        self._line.setFrameShape(QFrame.HLine)
        self._line.setFrameShadow(QFrame.Sunken)

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._setup_left_side_widget()
        self._image_preview = ImagePreview(self._file)
        self._layout.addWidget(self._image_preview)

    def _setup_left_side_widget(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        left_side_widget = QWidget()
        left_side_widget.setStyleSheet("max-width: 400px;")
        left_side_layout = QVBoxLayout()
        left_side_layout.setAlignment(Qt.AlignTop)
        left_side_widget.setLayout(left_side_layout)

        image_name_label = QLabel(f'Image: {self._file.name}', self)
        image_name_label.setAlignment(Qt.AlignLeft)
        image_name_label.setFont(font)
        image_name_label.setStyleSheet("max-height: 30px;")

        left_side_layout.addWidget(image_name_label)
        left_side_layout.addWidget(self._line)

        self._image_customization_form = ImageCustomizationForm()
        self._image_customization_form.customization_changed.connect(
            lambda customization: self._notify_image_preview(customization))

        left_side_layout.addWidget(self._image_customization_form)
        left_side_layout.addWidget(self._line)
        self._analysis_input_form = AnalysisInputParametersForm()
        left_side_layout.addWidget(self._analysis_input_form)

        continue_button = QPushButton("Continue", self)
        continue_button.clicked.connect(
            lambda: self._emit_parametrization_finished())
        left_side_layout.addWidget(continue_button)

        self._layout.addWidget(left_side_widget)

    def _emit_parametrization_finished(self):
        return self.analysis_parametrization_finished.emit(
            AnalysisParametrization2(
                self._file,
                self._image_customization_form.parametrization(),
                self._analysis_input_form.parametrization(),
                self._image_preview.image_selection()))

    def _notify_image_preview(self, customization):
        self._image_preview.apply_customization(customization)

    def handle_validation_errors(self, errors):
        self._image_customization_form.handle_errors(
            errors.for_image_customization_form())
        self._analysis_input_form.handle_errors(
            errors.for_analysis_input_form())
        self._image_preview.handle_errors(errors.for_image_preview())

    def customization_strategy(self):
        modal = ImageSettingsModal()
        return ParametersCustomizationStrategy(modal.exec())


class AnalysisParametrization(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
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
            self._dyssynchrony_configuration.set_image_customization_strategy(
                strategy)

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
        self._image_preview.set_image(self._image)

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
        self._image_preview = ImagePreview(self)
        self._image_preview.cropped.connect(self.set_cropping_coordinates)
        layout.addWidget(self._image_preview)
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

        filter_diameter_label = QLabel(
            "Diameter of each pixel neighborhood that is used during filtering",
            widget)
        filter_diameter_label.setWordWrap(True)
        self._filter_diameter_slider = QSlider(Qt.Horizontal, widget)
        self._filter_diameter_slider.setMinimum(1)
        self._filter_diameter_slider.setMaximum(40)
        self._filter_diameter_slider.setValue(1)
        self._filter_diameter_slider.valueChanged[int].connect(
            self._change_filter_diameter)

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
        self._filter_sigma_color_slider.valueChanged[int].connect(
            self._change_filter_sigma_color)

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
        self._filter_sigma_spatial_slider.valueChanged[int].connect(
            self._change_filter_sigma_spatial)

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

        slice_width_label = QLabel("The width (in pixels) of each slice",
                                   widget)
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
                NeedToSelectImageAreaToAnalyze().exec()
            else:
                if self._dyssynchrony_configuration.need_to_select_customization_strategy():
                    self._set_customization_strategy()

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
        alpha_contrast = float(131 * (self._contrast_value + 127)) / (
                127 * (131 - self._contrast_value))
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
        image = cv2.addWeighted(image, alpha_brightness, image, 0,
                                gamma_brightness)
        image = cv2.addWeighted(image, alpha_contrast, image, 0,
                                gamma_contrast)
        image = cv2.bilateralFilter(image, self._filter_diameter,
                                    self._sigma_color, self._sigma_spatial)
        self._image_preview.set_image(image)

    def set_cropping_coordinates(self, position1, position2):
        self._cropping_coordinates = {
            "x_start": int(min(position1.x(), position2.x())),
            "y_start": int(min(position1.y(), position2.y())),
            "x_end": int(max(position1.x(), position2.x())),
            "y_end": int(max(position1.y(), position2.y()))
        }

    def _get_image_path(self):
        path = self._form_data["path"]

        if os.path.isfile(path):
            return path
        else:
            return [f'{path}/{file}' for file in os.listdir(path) if
                    file.endswith(".tif")][0]
