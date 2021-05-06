import sys

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow

app = QApplication(sys.argv)

view = MainWindow()
view.showMaximized()

app.exec_()

if __name__ == "__main__":
    app.exec_()
