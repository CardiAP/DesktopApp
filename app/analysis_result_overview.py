from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class AnalysisResultOverview(QWidget):
    result_selected = Signal()

    def __init__(self, parent):
        super(AnalysisResultOverview, self).__init__(parent)
        self._image_name = None
        self._analysis_results = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self._tabs = None

    def _setup_tabs(self):
        if self._tabs is not None:
            self.layout.removeWidget(self._tabs)
            self._tabs.destroy()

        image_slices = self._analysis_results['slices']
        if len(image_slices) > 0:
            self._tabs = QTabWidget(self)
            for index, image_slice in enumerate(image_slices):
                intensities = image_slice['intensities']
                self._tabs.addTab(Plotter(self._tabs, intensities, range(len(intensities))), f"Slice {str(index)}")
            self.layout.addWidget(self._tabs)

    def set_analysis_results(self, results):
        self._analysis_results = results
        image_intensities = results['image']['intensities']
        self.layout.addWidget(Plotter(self, image_intensities, range(len(image_intensities))))
        self._setup_tabs()
        button = QPushButton("Add this image to the results")
        button.clicked.connect(lambda: self.result_selected.emit())
        self.layout.addWidget(button)


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
        self.axes.plot([] if y_axis is None else y_axis, [] if x_axis is None else x_axis)

        super(self.__class__, self).__init__(fig)

    def plot(self, x_axis, y_axis):
        self.axes.plot(y_axis, x_axis)
