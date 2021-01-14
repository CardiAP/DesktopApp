from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, \
    QHBoxLayout, QPushButton

from app.image_settings_modal import ImageSettingsModal
from app.models.analysis_parametrization import AnalysisParametrization, \
    ParametersCustomizationStrategy
from app.views.analysis_input_parameters_form import \
    AnalysisInputParametersForm
from app.views.image_customization_form import ImageCustomizationForm
from app.views.image_preview import ImagePreview


class AnalysisParametrizationForm(QWidget):
    analysis_parametrization_finished = pyqtSignal(AnalysisParametrization)
    go_back = pyqtSignal()

    def __init__(self, parametrization):
        super().__init__()
        self._file = parametrization.file
        self._setup(parametrization)

    def _setup(self, parametrization):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        self._line = QFrame(self)
        self._line.setFrameShape(QFrame.HLine)
        self._line.setFrameShadow(QFrame.Sunken)

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._setup_left_side_widget(parametrization)
        self._image_preview = ImagePreview(self._file, parametrization.image_customization, parametrization.image_selection)
        self._layout.addWidget(self._image_preview)

    def _setup_left_side_widget(self, parametrization):
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

        self._image_customization_form = ImageCustomizationForm(parametrization.image_customization)
        self._image_customization_form.customization_changed.connect(
            lambda customization: self._notify_image_preview(customization))

        left_side_layout.addWidget(self._image_customization_form)
        left_side_layout.addWidget(self._line)
        self._analysis_input_form = AnalysisInputParametersForm(parametrization.input_parameters)
        left_side_layout.addWidget(self._analysis_input_form)

        continue_button = QPushButton("Continue", self)
        continue_button.clicked.connect(
            lambda: self._emit_parametrization_finished())
        left_side_layout.addWidget(continue_button)

        self._layout.addWidget(left_side_widget)

    def _emit_parametrization_finished(self):
        return self.analysis_parametrization_finished.emit(
            AnalysisParametrization(
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
