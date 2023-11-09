# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from screen1_InceptionV3 import Screen1
from screen2_InceptionV3_own import Screen2
from screen3_YoloV8 import Screen3
from screen4_statistics import Screen4

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Multi-Screen App")
        self.setGeometry(100, 100, 800, 600)

        # Tworzymy centralny widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Dodajemy przyciski do przełączania ekranów
        self.buttons = {
            "Ekran1": QPushButton("Przejdź do Ekran1"),
            "Ekran2": QPushButton("Przejdź do Ekran2"),
            "Ekran3": QPushButton("Przejdź do Ekran3"),
            "Ekran4": QPushButton("Przejdź do Ekran4")
        }

        # Tworzymy instancje ekranów
        self.screens = {
            "Ekran1": Screen1(),
            "Ekran2": Screen2(),
            "Ekran3": Screen3(),
            "Ekran4": Screen4()
        }

        # Ustawiamy sygnały dla przycisków
        for name, button in self.buttons.items():
            self.layout.addWidget(button)
            button.clicked.connect(self.change_screen(name))

        self.current_screen = None

    def change_screen(self, screen_name):
        def show_screen():
            # Jeżeli mamy aktualnie wyświetlany ekran, ukrywamy go
            if self.current_screen:
                self.current_screen.hide()
            # Wyświetlamy wybrany ekran
            self.current_screen = self.screens[screen_name]
            self.layout.addWidget(self.current_screen)
            self.current_screen.show()
        return show_screen

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
