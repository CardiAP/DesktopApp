from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, \
    QGridLayout, QHBoxLayout, QDialog, QLabel, QDialogButtonBox, QStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, \
    NavigationToolbar2QT
from matplotlib.figure import Figure


class ImagesRefinement(QWidget):
    select_all_and_continue = pyqtSignal()
    continue_with_selected = pyqtSignal()

    def __init__(self, images_section, selected_images_section,
                 continue_validation):
        super(self.__class__, self).__init__()
        images_section.setParent(self)
        selected_images_section.setParent(self)

        self.setLayout(QVBoxLayout())
        self._continue_validation = continue_validation

        self._content_section = QWidget()
        self.layout().addWidget(self._content_section)
        self._content_section.setLayout(QGridLayout())

        self._images_section = images_section
        self._content_section.layout().addWidget(self._images_section, 0, 0, 1, 3, Qt.AlignTop)
        self._selected_images = selected_images_section
        self._content_section.layout().addWidget(self._selected_images, 0, 4,
                                                 1, 1, Qt.AlignTop)

        self._actions_section = QWidget(self)
        self.layout().addWidget(self._actions_section)

        self._setup_continue_buttons()

    def _setup_continue_buttons(self):
        self._actions_section.setLayout(QHBoxLayout())
        self._select_all_and_continue_button = QPushButton(
            "Select all and continue", parent=self)
        self._select_all_and_continue_button.clicked.connect(
            lambda: self._select_all_clicked())

        self._continue_button = QPushButton("Continue with selected results",
                                            parent=self)
        self._continue_button.clicked.connect(lambda: self._continue_clicked())

        self._actions_section.layout().addWidget(
            self._select_all_and_continue_button)
        self._actions_section.layout().addWidget(self._continue_button)

    def _select_all_clicked(self):
        self.select_all_and_continue.emit()

    def _continue_clicked(self):
        if self._continue_validation():
            self.continue_with_selected.emit()
        else:
            self._show_no_selected_result()

    def _show_no_selected_result(self):
        NeedToSelectResult().exec()


class ImageSection(QWidget):
    current_image_selected = pyqtSignal()

    def __init__(self, tabs, image_data_widget):
        super().__init__()
        tabs.setParent(self)
        image_data_widget.setParent(self)

        self.layout = (QVBoxLayout())
        self.layout.addWidget(tabs)
        self.layout.addWidget(image_data_widget)
        self.layout.addWidget(self._add_to_selected_images_button())

    def _add_to_selected_images_button(self):
        button = QPushButton("Select this image")
        button.clicked.connect(lambda: self.current_image_selected.emit())
        return button


class Tabs(QTabWidget):
    tab_changed_to = pyqtSignal(str)

    def __init__(self, names):
        super().__init__()
        for name in names:
            self.addTab(self._empty_widget(name), name)
        self.currentChanged.connect(
            lambda index: self._emit_tab_changed(index))

    def _emit_tab_changed(self, index):
        self.tab_changed_to(self.widget(index).objectName())

    def _empty_widget(self, name):
        widget = QWidget()
        widget.setObjectName(name)
        # widget.setVisible(False)
        return widget

    def current_tab_name(self):
        return self.widget(self.currentIndex()).objectName()

    def show_first_tab(self):
        self.setCurrentIndex(0)


class ImageData(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self._slices_data = {}
        self._plotter = QWidget()
        self._tabs = Tabs([])
        self._slice_plotter = QWidget()
        self._on_slice_tab_changed = lambda slice_name: self._tab_changed_to(
            slice_name)

    def _tab_changed_to(self, slice_name):
        slice_data = self._slices_data[slice_name]
        self.layout.removeWidget(self._slice_plotter)
        self._slice_plotter.destroy(True)
        self._slice_plotter = Plotter(self, slice_data, range(len(slice_data)))
        self.layout.addWidget(self._slice_plotter, 2, 0)

    def show_image(self, image_data, slices_data):
        self._slices_data = {}
        for index, slice_data in enumerate(slices_data):
            self._slices_data[f"Slice {index}"] = slice_data

        self._plot_image_data(image_data)
        self._show_slices()

    def _show_slices(self):
        self.layout.removeWidget(self._tabs)
        self._tabs.tab_changed_to.disconnect(self._on_slice_tab_changed)
        self._tabs.destroy(True)

        if self._slices_data != {}:
            self._tabs = Tabs(self._slices_data.keys())
            self._tabs.tab_changed_to.connect(self._on_slice_tab_changed)
            self.layout.addWidget(self._tabs, 1, 0)
            self._tabs.show_first_tab()
        else:
            self._tabs = QWidget()
            self._tabs.setVisible(False)
            self.layout.addWidget(self._tabs, 1, 0)

    def _plot_image_data(self, image_data):
        self.layout.removeWidget(self._plotter)
        self._plotter.destroy(True)
        self._plotter = Plotter(self, image_data, range(len(image_data)))
        self.layout.addWidget(self._plotter, 0, 0)


class Plotter(QWidget):
    def __init__(self, parent=None, x_axis=None, y_axis=None):
        super(self.__class__, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        plot = Plot(x_axis, y_axis)
        toolbar = NavigationToolbar2QT(plot, self)
        self.layout.addWidget(toolbar)
        self.layout.addWidget(plot)


class Plot(FigureCanvasQTAgg):
    def __init__(self, x_axis=None, y_axis=None):
        width = 5
        height = 4
        dpi = 100

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.plot([] if y_axis is None else y_axis,
                       [] if x_axis is None else x_axis)

        super(self.__class__, self).__init__(fig)

    def plot(self, x_axis, y_axis):
        self.axes.plot(y_axis, x_axis)


class NeedToSelectResult(QDialog):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel(
            'You need to select at least one image to continue, or if you want to select all the images please use the "Select all and continue" button')
        label.setWordWrap(True)
        button = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class SelectedImages(QWidget):
    image_removed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Selected images"),
                                Qt.AlignTop)
        self._selected_images_container = QWidget(parent=self)
        self.layout().addWidget(self._selected_images_container, Qt.AlignTop)

        self._selected_images_container.setLayout(QVBoxLayout())
        self._selected_images_widgets = []

    def set_selected_images(self, selected_images):
        for selected_image_widget in self._selected_images_widgets:
            selected_image_widget.deleteLater()

        self._selected_images_widgets = []

        for selected_image in selected_images:
            selected_image_widget = SelectedImage(
                self._selected_images_container, selected_image)
            selected_image_widget.remove_clicked.connect(
                lambda image_name: self.result_removed.emit(image_name))
            self._selected_images_container.layout().addWidget(
                selected_image_widget, Qt.AlignTop)
            self._selected_results.append(selected_image_widget)


class SelectedImage(QWidget):
    remove_clicked = pyqtSignal(int)

    def __init__(self, parent, selected_image):
        super().__init__(parent)
        self.setLayout(QGridLayout())
        self._label = QLabel(selected_image, parent=self)
        self._button = QPushButton(parent=self)
        self._button.setIcon(self.style().standardIcon(
            getattr(QStyle, "SP_DialogDiscardButton")))
        self._button.clicked.connect(
            lambda: self.remove_clicked.emit(selected_image))
        self._button.setToolTip("Remove this image from the selected results")
        self.layout().addWidget(self._label, 0, 1)
        self.layout().addWidget(self._button, 0, 2)
