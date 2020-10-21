from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QWidget, QLabel, QGridLayout


class DataPointsSelectionController(object):
    def __init__(self, results, view):
        self._view = view
        self._results = results
        self._image_checkboxes = self._build_checkboxes()
        self._slices_checkboxes = self._build_checkboxes()

        self._view.set_image_data_points_selection_form(
            self._build_data_points_selection_widget("Image data points selection", self._image_checkboxes))
        self._view.set_slices_data_points_selection_form(
            self._build_data_points_selection_widget("Slices data points selection", self._slices_checkboxes))

        self._view.continue_button.clicked.connect(lambda: self._continue_clicked())

    def _continue_clicked(self):
        if self._can_continue():
            self._set_selected_data()
            self._view.finished.emit()
        else:
            self._view.show_need_to_check_modal()

    def _set_selected_data(self):
        self._results.set_selected_image_data_points(self._get_selected_image_data_points())
        self._results.set_selected_slices_data_points(self._get_selected_slices_data_points())

    def _can_continue(self):
        return len(self._get_selected_image_data_points()) > 0 and len(self._get_selected_slices_data_points()) > 0

    def _get_selected_slices_data_points(self):
        return self._get_checked_checkbox_names(self._slices_checkboxes)

    def _get_selected_image_data_points(self):
        return self._get_checked_checkbox_names(self._image_checkboxes)

    def _get_checked_checkbox_names(self, checkboxes):
        return [name for name in checkboxes if checkboxes[name].isChecked()]

    def _build_data_points_selection_widget(self, title, checkboxes):
        widget = QWidget()

        layout = QGridLayout()
        widget.setLayout(layout)

        label = QLabel(parent=widget)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setText(title)
        label.setMaximumHeight(10)
        layout.addWidget(label, 0, 0, 1, 1)

        for index, key in enumerate(checkboxes):
            checkboxes[key].setParent(self._view)
            layout.addWidget(checkboxes[key], index + 1, 0, 1, 1)
        return widget

    def _build_checkboxes(self):
        return {
            'max_peaks': QCheckBox('Max peaks'),
            'min_peaks': QCheckBox('Min peaks'),
            'amplitudes': QCheckBox('Amplitudes'),
            'peak_time': QCheckBox('Peak times'),
            'half_peak_time': QCheckBox('Half peak times'),
            'taus': QCheckBox('Taus')
        }
