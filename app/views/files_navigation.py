from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from app.models.analysis_files import AnalysisFile
from app.views.clickable import Clickable


class File(QWidget):
    @classmethod
    def for_file(cls, parent, file):
        if file.is_unselected():
            return PendingFile(parent, file)
        elif file.is_selected():
            return SelectedFile(parent, file)
        elif file.is_accepted():
            return AcceptedFile(parent, file)
        else:
            raise ValueError(
                f"The file has an unexpected status {file.status}")

    def __init__(self, parent, file):
        super().__init__(parent)
        self.__file = file
        self.setLayout(QHBoxLayout(self))
        self.layout().addWidget(QLabel(self.__file.name))
        unchecked = QWidget()
        unchecked.setStyleSheet(
            f"border: 1px solid {self.color}; height: 5px; width: 5px")
        self.layout().addWidget(unchecked)


class SelectedFile(File):
    @property
    def color(self):
        return 'blue'


class AcceptedFile(File):
    @property
    def color(self):
        return 'green'


class PendingFile(File):
    @property
    def color(self):
        return 'black'


class FileSelector(Clickable):
    def __init__(self, parent, file):
        super().__init__(parent)
        self.__file = file
        self.setLayout(QHBoxLayout(self))
        self.layout().addWidget(PendingFile(self, self.__file))

    @property
    def file(self):
        return self.__file


class FilesNavigation(QWidget):
    file_clicked = Signal(AnalysisFile)

    def __init__(self, selected_files):
        super().__init__()
        self.setLayout(QVBoxLayout(self))
        self.__file_widgets = []
        for file in selected_files:
            file_selector = FileSelector(self, file)
            file_selector.clicked.connect(
                self.file_clicked_trigger(file_selector))
            self.__file_widgets.append(file_selector)
            self.layout().addWidget(file_selector)

    def file_clicked_trigger(self, file_selector):
        return lambda: self.fire_file_clicked(file_selector.file)

    def fire_file_clicked(self, file):
        self.file_clicked.emit(file)
