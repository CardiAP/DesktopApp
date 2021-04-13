from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, \
    QPushButton, QFileDialog, QGridLayout, QGroupBox

from app.models.new_analysis import NewAnalysisParametrization
from app.views.input_error_message import InputErrorMessage


class AnalysisTypeSelection(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        group_box = QGroupBox("Select analysis type", self)
        group_box_layout = QVBoxLayout(group_box)

        self.layout.addWidget(group_box)
        self.__radio_buttons = [
            self.__build_radio_button_with("Transitory",
                                           NewAnalysisParametrization.TRANSITORY,
                                           group_box_layout),
            self.__build_radio_button_with("Waves",
                                           NewAnalysisParametrization.WAVES,
                                           group_box_layout),
            self.__build_radio_button_with("Sparks",
                                           NewAnalysisParametrization.SPARKS,
                                           group_box_layout)
        ]

        self.__error = InputErrorMessage("You need to select an analysis type")
        self.layout.addWidget(self.__error)
        self.__error.setVisible(False)

    def __build_radio_button_with(self, label, analysis_type, layout):
        radiobutton = QRadioButton(label)
        radiobutton.analysis_type = analysis_type
        layout.addWidget(radiobutton)
        radiobutton.clicked.connect(lambda: self.clear_errors())
        return radiobutton

    def clear_errors(self):
        self.__error.setVisible(False)

    def show_error(self):
        self.__error.setVisible(True)

    def selected_analysis_type(self):
        return next((radio_button for radio_button in self.__radio_buttons if
                     radio_button.isChecked()), None)


class AnalysisImagesSelection(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.__selected_files = []

        select_images_button = QPushButton(
            "Select the images you want to analyze", self)
        select_images_button.clicked.connect(self.__open_file_selector)
        self.layout.addWidget(select_images_button)

        self.__error = InputErrorMessage(
            "You need to select at least one .tif image")
        self.layout.addWidget(self.__error)
        self.__error.setVisible(False)

        self.__selected_files_list = QWidget()
        self.layout.addWidget(self.__selected_files_list)
        self.__show_selected_files_list()

    def __show_selected_files_list(self):
        self.layout.removeWidget(self.__selected_files_list)
        self.__selected_files_list.deleteLater()

        self.__selected_files_list = QWidget()
        self.layout.addWidget(self.__selected_files_list)
        self.__selected_files_list.setStyleSheet("border: 1px solid black; padding: 2px")
        self.__selected_files_list.setLayout(QVBoxLayout())

        for file in self.__selected_files:
            label = QLabel(file, self.__selected_files_list)
            label.setStyleSheet("border: unset; padding: unset")
            self.__selected_files_list.layout().addWidget(label)

    def __open_file_selector(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setMimeTypeFilters(["image/tiff"])
        dlg.setNameFilter("*.tif")
        dlg.setFileMode(QFileDialog.ExistingFiles)

        if dlg.exec_():
            self.__selected_files = dlg.selectedFiles()
            self.clear_errors()
            self.__show_selected_files_list()

    def clear_errors(self):
        self.__error.setVisible(False)

    def show_error(self):
        self.__error.setVisible(True)

    def selected_files(self):
        return self.__selected_files


class InputSection(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.__analysis_type_selection = AnalysisTypeSelection(self)
        self.layout.addWidget(self.__analysis_type_selection, 0, 0)
        self.__analysis_images_selection = AnalysisImagesSelection(self)
        self.layout.addWidget(self.__analysis_images_selection, 0, 1)

    def clear_errors(self):
        self.__analysis_images_selection.clear_errors()
        self.__analysis_type_selection.clear_errors()

    def show_no_type_selected_error(self):
        self.__analysis_type_selection.show_error()

    def show_no_files_selected(self):
        self.__analysis_images_selection.show_error()

    def selected_analysis_type(self):
        return self.__analysis_type_selection.selected_analysis_type()

    def selected_files(self):
        return self.__analysis_images_selection.selected_files()


class NewAnalysisView(QWidget):
    finished = pyqtSignal(NewAnalysisParametrization)

    def __init__(self):
        super().__init__()
        self.__input_section_widget = None
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.__setup_ui()

    def __setup_ui(self):
        self.__set_title()
        self.__set_inputs_section()
        self.__set_actions_section()

    def __set_title(self):
        label = QLabel(self)
        label.setText("<h1>CardiAP</h1>")
        self.layout.addWidget(label)

    def __set_inputs_section(self):
        self.__input_section_widget = InputSection(self)
        self.layout.addWidget(self.__input_section_widget)

    def __set_actions_section(self):
        button = QPushButton("Continue")
        button.clicked.connect(lambda: self.__emit_finished_signal())
        self.layout.addWidget(button, alignment=Qt.AlignRight)

    def __emit_finished_signal(self):
        self.finished.emit(NewAnalysisParametrization(
            self.__input_section_widget.selected_files(),
            self.__input_section_widget.selected_analysis_type()))

    def show_errors(self, errors):
        self.__input_section_widget.clear_errors()
        if NewAnalysisParametrization.NO_TYPE_SELECTED in errors:
            self.__input_section_widget.show_no_type_selected_error()
        if NewAnalysisParametrization.NO_FILES_SELECTED in errors:
            self.__input_section_widget.show_no_files_selected()
