from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTabWidget, \
    QHBoxLayout, QPushButton, QDialog, QLabel, QDialogButtonBox, QFileDialog, \
    QLineEdit, QFormLayout, QCheckBox, QFrame

from app.controllers.data_export_controller import DataExportController


class DataExport(QWidget):
    finished = pyqtSignal()
    export_format_selected = pyqtSignal(str)
    directory_changed = pyqtSignal(str)
    finish_with_settings = pyqtSignal()

    def __init__(self):
        super(DataExport, self).__init__()
        self.setLayout(QVBoxLayout())

        self._content_section = QWidget()
        self.layout().addWidget(self._content_section)
        self._content_section.setLayout(QGridLayout())

        self._results_data = QTabWidget(self)
        self._content_section.layout().addWidget(self._results_data, 0, 0)

        self._actions_section = QWidget(self)
        self.layout().addWidget(self._actions_section)

        self._setup_continue_buttons()
        self._setup_settings_modal()

    def _setup_settings_modal(self):
        self._dialog = DataExportSettings()
        self._dialog.export_format_selected.connect(
            self.export_format_selected.emit)
        self._dialog.finish_with_settings.connect(
            self.finish_with_settings.emit)
        self._dialog.directory_changed.connect(self.directory_changed.emit)

    def _setup_continue_buttons(self):
        self._actions_section.setLayout(QHBoxLayout())
        self.export_button = QPushButton("Export results", parent=self)
        self._actions_section.layout().addWidget(self.export_button)

    def set_results_data(self, view):
        self._content_section.layout().removeWidget(self._results_data)
        self._results_data.deleteLater()
        self._results_data = view
        self._results_data.setParent(self)
        self._content_section.layout().addWidget(self._results_data, 0, 0)
        self._results_data.currentChanged.emit(0)

    def complete_export_settings(self):
        self._dialog.exec()

    def need_to_complete_directory(self):
        self._dialog.need_to_complete_directory()

    def need_to_complete_export_format(self):
        self._dialog.need_to_complete_export_format()


class DataExportSettings(QDialog):
    export_format_selected = pyqtSignal(str)
    directory_changed = pyqtSignal(str)
    finish_with_settings = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel(
            'Please select the path and the file format for the export')
        label.setWordWrap(True)

        file_path_form = QWidget()
        file_path_form_layout = QFormLayout(file_path_form)

        path_label = QLabel("Selected directory", file_path_form)
        self.path_input = QLineEdit(file_path_form)
        self.path_input.setReadOnly(True)
        select_path_button = QPushButton("Select the directory")
        select_path_button.clicked.connect(self.select_path)

        file_path_form_layout.setWidget(0, QFormLayout.LabelRole, path_label)
        file_path_form_layout.setWidget(0, QFormLayout.FieldRole,
                                        self.path_input)
        file_path_form_layout.setWidget(1, QFormLayout.LabelRole,
                                        select_path_button)

        file_path_form.setLayout(file_path_form_layout)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        csv_checkbox = QCheckBox()
        csv_checkbox.setText('CSV')
        csv_checkbox.clicked.connect(lambda: self.export_format_selected.emit(DataExportController.CSV_FORMAT))

        json_checkbox = QCheckBox()
        json_checkbox.setText('JSON')
        json_checkbox.clicked.connect(lambda: self.export_format_selected.emit(DataExportController.JSON_FORMAT))

        xslx_checkbox = QCheckBox()
        xslx_checkbox.setText('XSLX')
        xslx_checkbox.clicked.connect(lambda: self.export_format_selected.emit(DataExportController.XLSX_FORMAT))

        format_form = QWidget()
        format_form_layout = QFormLayout()
        format_form.setLayout(format_form_layout)
        format_form_layout.setWidget(0, QFormLayout.FieldRole, csv_checkbox)
        format_form_layout.setWidget(1, QFormLayout.FieldRole, json_checkbox)
        format_form_layout.setWidget(2, QFormLayout.FieldRole, xslx_checkbox)

        ok_button = QPushButton('Save data')
        ok_button.clicked.connect(self.finish_with_settings.emit)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(ok_button, QDialogButtonBox.ActionRole)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(file_path_form)
        self.layout.addWidget(line)
        self.layout.addWidget(format_form)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def need_to_complete_export_format(self):
        DataExportSettingsMessage("Please select at least one file format").exec()

    def need_to_complete_directory(self):
        DataExportSettingsMessage(
            "Please select at the directory to save the data").exec()

    def select_path(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select the directory where you want to save the analysis",
            "",
            options=options
        )
        self.path_input.setText(directory)
        self.directory_changed.emit(directory)


class DataExportSettingsMessage(QDialog):
    def __init__(self, message):
        super(self.__class__, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel(message)
        label.setWordWrap(True)
        button = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
