import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow

app = QApplication(sys.argv)

view = MainWindow()
view.showMaximized()

sys.exit(app.exec_())