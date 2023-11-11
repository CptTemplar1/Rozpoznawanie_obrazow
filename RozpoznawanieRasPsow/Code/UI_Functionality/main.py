import sys
import platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

# GUI FILE
from ui_main import Ui_MainWindow

# IMPORT FUNCTIONS
from ui_functions import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## TOGGLE/BURGUER MENU
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        ## PAGES
        # PAGE 1
        ########################################################################
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))

        # Dodaj funkcję do otwierania eksploratora plików i wczytywania obrazu do Labela PictureLabel
        self.ui.PictureLabel.mousePressEvent = self.openFileDialog
        ########################################################################


        # PAGE 2
        ########################################################################
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        ########################################################################


        # PAGE 3
        ########################################################################
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        ########################################################################


        # PAGE 4
        ########################################################################
        self.ui.btn_page_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        ########################################################################


        ## SHOW ==> MAIN WINDOW
        self.show()
        ## ==> END ##

    #Funkcja otwierająca eksplorator plików i wczytująca obraz do Labela PictureLabel
    def openFileDialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        fileName, _ = QFileDialog.getOpenFileName(self, "Wybierz plik obrazu", "", "Images (*.png *.jpg *.bmp *.gif *.jpeg);;All Files (*)", options=options)

        if fileName:
            pixmap = QPixmap(fileName)
            self.ui.PictureLabel.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())