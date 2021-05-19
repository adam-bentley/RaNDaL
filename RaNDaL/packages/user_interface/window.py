import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QGridLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(600, 600, 600, 600)
        self.setStyleSheet("background-color: black; border: 1px solid white")

        # Layout
        layout = QGridLayout()
        self.ui_components(layout)
        self.setLayout(layout)

        self.show()

    def ui_components(self, layout):
        label = QLabel(self)
        pixmap = QPixmap("..//data//test_images//0.jpg")
        pixmap = pixmap.scaledToWidth(int(pixmap.width()/2), 0)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        layout.addWidget(label)

        self.showMaximized()


App = QApplication(sys.argv)
window = MainWindow()
sys.exit(App.exec())
