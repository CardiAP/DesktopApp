from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from app.result_data_table import ResultDataTable


class ResultDataVisualization(QWidget):
    def __init__(self, parent):
        super(ResultDataVisualization, self).__init__()
        self.setParent(parent)
        self._image_data = {}
        self._slices_data = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self._tabs = None

    def _set_slices_data(self):
        if self._tabs is not None:
            self.layout.removeWidget(self._tabs)
            self._tabs.deleteLater()

        if len(self._slices_data) > 0:
            self._tabs = QTabWidget(self)
            for index, slice_data in enumerate(self._slices_data):
                self._tabs.addTab(ResultDataTable(self._tabs, slice_data), f"Slice {str(index)}")
            self.layout.addWidget(self._tabs)

    def set_data(self, image_data, slices_data):
        self._image_data = image_data
        self._slices_data = slices_data
        self.layout.addWidget(ResultDataTable(self, self._image_data))
        self._set_slices_data()