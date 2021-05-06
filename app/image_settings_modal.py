from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class ImageSettingsModal(QDialog):

    def __init__(self):
        super(ImageSettingsModal, self).__init__()

        self.setWindowTitle("CardiAP")

        label = QLabel("I see that you have selected several images to analyze. Do you want to apply the same customization to all the images?")
        label.setWordWrap(True)
        button = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
