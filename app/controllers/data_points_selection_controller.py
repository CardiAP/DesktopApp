from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QWidget, QLabel, QGridLayout


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
        return self._get_checked_checkbox_ids(self._slices_checkboxes)

    def _get_selected_image_data_points(self):
        return self._get_checked_checkbox_ids(self._image_checkboxes)

    def _get_checked_checkbox_ids(self, checkboxes):
        return [checkboxes[name].data_point_id for name in checkboxes if checkboxes[name].isChecked()]

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
            'max_peaks_positions': self._build_checkbox('Max peaks position', 'max_peaks_positions'),
            'max_peaks_intensities': self._build_checkbox('Max peaks intensities', 'max_peaks_intensities'),
            'min_peaks_positions': self._build_checkbox('Min peaks positions', 'min_peaks_positions'),
            'min_peaks_intensities': self._build_checkbox('Min peaks intensities', 'min_peaks_intensities'),
            'amplitudes': self._build_checkbox('Amplitudes', 'amplitudes'),
            'peak_time': self._build_checkbox('Peak times', 'times_to_peaks'),
            'half_peak_time': self._build_checkbox('Half peak times', 'times_to_half_peaks'),
            'taus': self._build_checkbox('Taus', 'tau_s')
        }

    def _build_checkbox(self, name, id):
        checkbox = QCheckBox()
        checkbox.setText(name)
        checkbox.data_point_id = id
        return checkbox
