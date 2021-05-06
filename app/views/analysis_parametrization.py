from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, \
    QHBoxLayout

from app.models.analysis_parametrization import AnalysisParametrization
from app.views.analysis_input_parameters_form import \
    AnalysisInputParametersForm
from app.views.image_customization_form import ImageCustomizationForm
from app.views.image_preview import ImagePreview


class AnalysisParametrizationForm(QWidget):

    def __init__(self, parametrization):
        super().__init__()
        self.__setup(parametrization)

    def __setup(self, parametrization):
        self.__line = QFrame(self)
        self.__line.setFrameShape(QFrame.HLine)
        self.__line.setFrameShadow(QFrame.Sunken)

        self.setLayout(QHBoxLayout(self))
        self.__setup_left_side_widget(parametrization)
        self.__image_preview = ImagePreview(
            parametrization.file,
            parametrization.image_customization,
            parametrization.image_selection)
        self.layout().addWidget(self.__image_preview)

    def __setup_left_side_widget(self, parametrization):
        left_side_widget = QWidget()
        left_side_widget.setStyleSheet("max-width: 400px;")
        left_side_layout = QVBoxLayout()
        left_side_layout.setAlignment(Qt.AlignTop)
        left_side_widget.setLayout(left_side_layout)

        self.__image_customization_form = ImageCustomizationForm(
            parametrization.image_customization)
        self.__image_customization_form.customization_changed.connect(
            lambda customization: self.__notify_image_preview(customization))

        left_side_layout.addWidget(self.__image_customization_form)
        left_side_layout.addWidget(self.__line)
        self.__analysis_input_form = AnalysisInputParametersForm(
            parametrization.input_parameters)
        left_side_layout.addWidget(self.__analysis_input_form)

        self.layout().addWidget(left_side_widget)

    def get_parametrization(self):
        return self.analysis_parametrization_finished.emit(
            AnalysisParametrization(
                self._file,
                self.__image_customization_form.parametrization(),
                self.__analysis_input_form.parametrization(),
                self.__image_preview.image_selection()))

    def __notify_image_preview(self, customization):
        self.__image_preview.apply_customization(customization)

    def handle_validation_errors(self, errors):
        self.__image_customization_form.handle_errors(
            errors.for_image_customization_form())
        self.__analysis_input_form.handle_errors(
            errors.for_analysis_input_form())
        self.__image_preview.handle_errors(errors.for_image_preview())
