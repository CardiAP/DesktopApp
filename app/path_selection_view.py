from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QVBoxLayout, QPushButton, QLabel


class PathSelectionView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CariAP')
        self.setFixedSize(400, 400)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        QLabel('<h1>Hello World!</h1>', parent=self._centralWidget)
