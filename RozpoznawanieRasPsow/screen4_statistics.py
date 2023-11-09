# screen4.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Screen4(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Ekran nr 4")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)