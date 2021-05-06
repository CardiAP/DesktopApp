from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractScrollArea, QLabel


class ResultDataTable(QWidget):
    def __init__(self, parent, data):
        super(ResultDataTable, self).__init__()
        self.setParent(parent)
        self._data = data
        self.setLayout(QVBoxLayout())
        self._table = QTableWidget(self)
        self.layout().addWidget(self._table)

        self._table.setColumnCount(len(self._data) + 1)
        self._table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self._table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self._table.setCellWidget(0, 0, QWidget(self))

        should_set_row_count = True
        for data_point_index, data_point in enumerate(self._data):
            if should_set_row_count:
                self._table.setRowCount(len(self._data[data_point]))
                should_set_row_count = False

            column = data_point_index + 1
            label = QLabel(data_point)
            label.setAlignment(Qt.AlignCenter)
            self._table.setCellWidget(0, column, label)


            data_point_data = self._data[data_point]
            for data_index, _ in enumerate(data_point_data):
                row = data_index + 1
                label = QLabel(f'Peak {str(row)}')
                label.setAlignment(Qt.AlignCenter)
                self._table.setCellWidget(row, 0, label)

            for data_index, datum in enumerate(data_point_data):
                row = data_index + 1
                label = QLabel(str(datum))
                label.setAlignment(Qt.AlignCenter)
                self._table.setCellWidget(row, column, label)

        self._table.resizeColumnsToContents()