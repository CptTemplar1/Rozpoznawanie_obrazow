import sys
import platform

from PIL.ImageQt import ImageQt
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QImage)
from PySide6.QtWidgets import *
from PIL import Image
from keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.src.saving.saving_api import load_model
from ultralytics import YOLO
import numpy as np

# GUI FILE
from ui_main import Ui_MainWindow


class MainWindow(QMainWindow):
    # Zmienna przechowująca ścieżkę do ostatnio wczytanego obrazu
    lastly_uploaded_picture = None

    # Zmienne okreslające poszczególne modele sieci neuronowych
    inceptionv3_model = InceptionV3(weights='imagenet')
    our_inceptionv3_model = load_model('C:/Users/micha/OneDrive/Pulpit/InceptionV3/model_inception.h5')
    our_yolov8_model = YOLO("D:/GitHub/Rozpoznawanie_obrazow/RozpoznawanieRasPsow/Models/YoloV8_own//best.pt")

    # Zmienna przechowująca aktualnie wybrany model
    selected_model = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Wywołanie metody ustawiającej wartość labela oraz model w zmiennej na podstawie wybranego modelu z ComboBoxa
        self.update_label_and_model()
        # Wywoływanie tej metody za każdym razem przy zmianie wybranego modelu w ComboBoxie
        self.ui.modelComboBox.currentIndexChanged.connect(self.update_label_and_model())

        # PAGES
        # PAGE 1
        ########################################################################
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))

        # Dodaj funkcję do otwierania eksploratora plików i wczytywania obrazu do Labela uploadedPictureLabel
        self.ui.uploadedPictureLabel.mousePressEvent = self.select_and_display_image

        # Wywołanie metody przewidującej rasę psa po kliknięciu przycisku
        # Odpowiednia metoda jest wywoływana w funkcji on_detect_breed_button_clicked w zależności od wybranego modelu
        self.ui.detectBreedButton.clicked.connect(self.on_detect_breed_button_clicked)
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

    # Funkcja aktualizująca etykietę oraz wybrany model na podstawie wybranego modelu w ComboBoxie
    def update_label_and_model(self):
        selected_model = self.ui.modelComboBox.currentText()
        # Ustawienie formatowania etykiety
        style = "color: white; font-weight: bold;"
        self.ui.selectedModelLabel.setStyleSheet(style)
        self.ui.selectedModelLabel.setText(f"{selected_model}")

        # Ustawienie aktualnie wybranego modelu w zmiennej selected_model
        if self.ui.modelComboBox.currentIndex() == 0:
            self.selected_model = self.inceptionv3_model
        elif self.ui.modelComboBox.currentIndex() == 2:
            self.selected_model = self.our_inceptionv3_model
        elif self.ui.modelComboBox.currentIndex() == 3:
            self.selected_model = self.our_yolov8_model

    # Funkcja wywoływana po kliknięciu przycisku rozpoznawania rasy psa
    # Sprawdza, który model jest wybrany i wywołuje odpowiednią funkcję
    def on_detect_breed_button_clicked(self):
        index = self.ui.modelComboBox.currentIndex()
        if index == 0:
            self.predict_dog_breed_inceptionV3()
        elif index == 1:
            return
            # metoda dla our_incetionv3_model
        elif index == 2:
            return
            # metoda dla our_yolo_model

    #Funckja otwierająca eksplorator plików i wczytująca obraz do Labela uploadedPictureLabel
    def select_and_display_image(self, event):
        global lastlyUploadedPicture
        # Otwórz okno wyboru pliku
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            lastlyUploadedPicture = file_path
            # Wczytaj i przeskaluj obraz
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Wyświetl obraz
            self.ui.uploadedPictureLabel.setPixmap(pixmap)

    # Funkcja do przewidywania rasy psa na podstawie obrazu przy pomocy modelu InceptionV3
    def predict_dog_breed_inceptionV3(self):
        try:
            img = image.load_img(self.lastly_uploaded_picture, target_size=(299, 299))
            img_array = image.img_to_array(img)

            img = np.expand_dims(img_array, axis=0)
            img = preprocess_input(img)

            predictions = self.selected_model.predict(img)
            decoded_predictions = decode_predictions(predictions, top=1)[0]
            predicted_breed = decoded_predictions[0][1]

            self.ui.detectedBreedLabel.setText(f"{predicted_breed}")
        except Exception as e:
            self.ui.detectedBreedLabel.setText(f"Błąd: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
