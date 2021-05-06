from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton


class AnalysisView(QWidget):
    save_requested = Signal()

    def __init__(self, image_analysis, images_navigation):
        super().__init__()
        image_analysis.setParent(self)
        images_navigation.setParent(self)
        self.setLayout(QGridLayout(self))

        self.layout().addWidget(image_analysis, 0, 0, 1, 1)
        self.layout().addWidget(images_navigation, 0, 1, 1, 1)

        self.__button = QPushButton("Save Results")
        self.__button.clicked.connect(lambda: self.save_requested.emit())
        self.layout().addWidget(self.__button, 1, 0, 1, 2)


