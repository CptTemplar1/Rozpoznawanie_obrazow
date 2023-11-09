# screen3.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Screen3(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Ekran nr 3")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)