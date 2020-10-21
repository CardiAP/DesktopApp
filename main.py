import sys
import cv2

from PyQt5.QtWidgets import QApplication

from app.main_window import MainWindow

app = QApplication(sys.argv)

view = MainWindow()
view.showMaximized()

app.exec()

if __name__ == "__main__":
    app.exec()
