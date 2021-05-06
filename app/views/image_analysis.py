from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout

from app.views.analysis_parametrization import AnalysisParametrizationForm


class ImageAnalysisLayout(QWidget):
    def __init__(self, parent, file, parametrization_widget):
        super().__init__(parent)
        self.__file = file
        self.__parametrization_widget = parametrization_widget

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(QLabel(self.__file.name))
        self.layout().addWidget(parametrization_widget)

        self.graphics_button = QPushButton("View graphics")
        self.data_tables_button = QPushButton("View data tables")
        buttons_widget = QWidget()
        buttons_widget.setLayout(QHBoxLayout(buttons_widget))
        buttons_widget.layout().setAlignment(Qt.AlignLeft)
        buttons_widget.layout().addWidget(self.graphics_button)
        buttons_widget.layout().addWidget(self.data_tables_button)
        self.layout().addWidget(buttons_widget)

        self.discard_button = QPushButton("Discard")
        self.accept_button = QPushButton("Accept")
        action_buttons_widget = QWidget()
        action_buttons_widget.setLayout(QHBoxLayout(action_buttons_widget))
        action_buttons_widget.layout().setAlignment(Qt.AlignRight)
        action_buttons_widget.layout().addWidget(self.discard_button)
        action_buttons_widget.layout().addWidget(self.accept_button)
        self.layout().addWidget(action_buttons_widget)


class ImageAnalysis(QWidget):
    def __init__(self):
        super().__init__()

    def open_file(self):
        raise NotImplemented()


class TransitoryImageAnalysis(QWidget):
    accepted = Signal()
    discard = Signal()
    graphics_request = Signal()
    data_tables_request = Signal()

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.__initial_widget())
        self.__image_analysis_layout = None
        self.__parametrization_form = None

    def __initial_widget(self):
        widget = QWidget(self)
        widget.setLayout(QVBoxLayout(widget))
        widget.layout().setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(15)

        label = QLabel(
            "Please select one of the files on the right to analyze ->")
        label.setWordWrap(True)
        label.setFont(font)

        widget.layout().addWidget(label)

        return widget

    def set_for_analysis(self, file):
        QWidget().setLayout(self.layout())
        self.setLayout(QVBoxLayout())
        self.__parametrization_form = AnalysisParametrizationForm(
            file.parametrization)

        self.__image_analysis_layout = ImageAnalysisLayout(
            self, file, self.__parametrization_form)

        self.layout().addWidget(self.__image_analysis_layout)

        self.__image_analysis_layout.accept_button.clicked.connect(
            self.accepted.emit)

        self.__image_analysis_layout.discard_button.clicked.connect(
            self.discard.emit)

        self.__image_analysis_layout.graphics_button.clicked.connect(
            self.graphics_request.emit)

        self.__image_analysis_layout.data_tables_button.clicked.connect(
            self.data_tables_request.emit)

    def __get_parametrization_form(self):
        if self.__parametrization_form:
            return self.__parametrization_form
        else:
            raise ValueError("The parametrization form can not be None")

    def get_parametrization(self):
        self.__get_parametrization_form().get_parametrization()

    def show_validation_errors(self, validation_errors):
        self.__get_parametrization_form().handle_validation_errors(
            validation_errors)
