import sys
import platform

import cv2
from PIL.ImageQt import ImageQt
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, QThread, Signal, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QImage)
from PySide6.QtMultimedia import QCamera
from PySide6.QtWidgets import *
from PIL import Image
from keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.src.saving.saving_api import load_model
from ultralytics import YOLO
import numpy as np
import json
import mysql.connector
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

# GUI FILE
from ui_main import Ui_MainWindow


# Klasy do obsługi bazy danych
##################################################################################################################################################################################
class DatabaseConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="RozpoznawanieRasPsow"
        )
        self.cursor = self.connection.cursor()

    # Funkcja dodająca rekord do tabeli statystyk dla danego modelu
    def insert_result_record(self, table_name, predicted_breed, actual_breed):
        query = f"INSERT INTO {table_name} (predicted_breed, actual_breed) VALUES (%s, %s)"
        values = (predicted_breed, actual_breed)
        self.cursor.execute(query, values)
        self.connection.commit()

    # Funkcja pobierająca wszystkie rekordy z tabeli statystyk dla danego modelu
    def get_all_results(self, table_name):
        query = f"SELECT predicted_breed, actual_breed FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

# Klasy do obsługi kamery w oddzielnym wątku
##################################################################################################################################################################################
class CameraThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def run(self):
        # Użycie pierwszej dostępnej kamery
        cap = cv2.VideoCapture(0)

        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            else:
                break

        # Zwolnienie kamery po zakończeniu
        cap.release()


# Klasa okna kamery
class CameraWindow(QWidget):
    # Zmienna przechowująca obraz w postaci numpy array
    cv2_img = None

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.image_label = QLabel("Zdjęcie pojawi się tutaj")
        self.capture_button = QPushButton("Zrób zdjęcie")
        self.capture_button.clicked.connect(self.capture_image)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.capture_button)

        self.setLayout(self.layout)

        # Wątek kamery
        self.thread = CameraThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @Slot(np.ndarray)
    def update_image(self, cv_img):
        """ Aktualizacja obrazu w QLabel """
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        self.cv_img = cv_img

    def capture_image(self):
        """ Zatrzymuje wątek kamery i przekazuje obraz do MainWindow """
        self.thread.terminate()
        self.main_window.set_captured_image(self.image_label.pixmap(), self.cv_img)
        self.close()

    def convert_cv_qt(self, cv_img):
        """ Konwersja obrazu OpenCV na QPixmap """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)


# Klasa głównego okna aplikacji
##################################################################################################################################################################################
class MainWindow(QMainWindow):
    # Zmienna przechowująca ostatnio wczytany obraz w postaci Image
    lastly_uploaded_picture = None

    # Zmienne okreslające poszczególne modele sieci neuronowych
    inceptionv3_model = InceptionV3(weights='imagenet')
    yolov8_own_model = YOLO("Models/YoloV8_own/best.pt")
    if platform.node() == "LAPTOP-BPEJBCSR":
        inceptionv3_own_model = load_model('D:/Moje dane/Studia/Semestr_VII/Rozpoznawanie_mowy_i_obrazu/Projekt/InceptionV3/InceptionV3_own_60epochs/InceptionV3_60epochs.h5')
    elif platform.node() == "LAPTOP-KBH72I04":
        inceptionv3_own_model = load_model('C:/Users/przem/Desktop/model_inception.h5')
    elif platform.node() == "LAPTOP-SGU0S8R4":
        inceptionv3_own_model = load_model('C:/Users/dawch/Downloads/model_inception.h5')

    # Załadowanie słownika etykiet z pliku JSON dla naszego własnego modelu InceptionV3
    # Teraz można użyć tego słownika do mapowania indeksów na etykiety
    with open('Models/InceptionV3_own/class_indices.json') as json_file:
        labels = json.load(json_file)

    # Załadowanie pliku z listą ras psów, aby ograniczyć wyniki do samych ras psów w modelu InceptionV3
    with open('Models/InceptionV3/class_restrictions.json') as json_file:
        dog_breeds_data = json.load(json_file)
        dog_breeds_list = dog_breeds_data.get("dog_breeds", [])

    # Zmienna przechowująca nazwę tabeli w bazie danych dla aktualnie wybranego modelu
    selected_model_table_name = None

    def __init__(self, db_connector):
        QMainWindow.__init__(self)
        self.db_connector = db_connector
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Ustawienie domyślnego widoku przy starcie na pierwszą stronę
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)

        # Wywołanie metody ustawiającej wartość labela oraz model w zmiennej na podstawie wybranego modelu z ComboBoxa
        self.update_label_and_model()
        # Wywoływanie tej metody za każdym razem przy zmianie wybranego modelu w ComboBoxie
        self.ui.modelComboBox.currentIndexChanged.connect(self.update_label_and_model)

        # PAGES
        # PAGE 1
        ########################################################################
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))

        # Dodaj funkcję do otwierania eksploratora plików i wczytywania obrazu do Labela uploadedPictureLabel
        self.ui.uploadedPictureLabel.mousePressEvent = self.select_and_display_image

        # Wywołanie metody przewidującej rasę psa po kliknięciu przycisku
        # Odpowiednia metoda jest wywoływana w funkcji on_detect_breed_button_clicked w zależności od wybranego modelu
        self.ui.detectBreedButton.clicked.connect(self.on_detect_breed_button_clicked)

        # Wywołanie metody otwierającej kamerę po kliknięciu przycisku
        self.ui.openCameraButton.clicked.connect(self.open_camera)

        ########################################################################

        # PAGE 2
        ########################################################################
        self.ui.btn_page_2.clicked.connect(self.navigate_to_confusion_matrix_page)
        ########################################################################

        # Pokaż główne okno
        self.show()

# Funkcje związane z przechodzeniem do strony Confusion Matrix i generowaniem Confusion Matrix
##################################################################################################################################################################################
    # Funkcja przechodząca do strony Confusion Matrix i wywołująca funkcję generującą Confusion Matrix
    def navigate_to_confusion_matrix_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.generate_confusion_matrix()


    # Funkcja generująca Confusion Matrix dla aktualnie wybranego modelu i wyświetlająca go w Labelu matrix_label jako PixMap
    # Funkcja generująca Confusion Matrix dla aktualnie wybranego modelu i wyświetlająca go w Labelu matrix_label jako PixMap
    def generate_confusion_matrix(self):
        # Pobranie danych z bazy danych
        data = self.db_connector.get_all_results(self.selected_model_table_name)
        df = pd.DataFrame(data, columns=['predicted_breed', 'actual_breed'])

        # Zestaw unikalnych nazw ras psów
        unique_breeds = set(df['predicted_breed'].unique()) | set(df['actual_breed'].unique())

        # Tworzenie Confusion Matrix
        conf_matrix = confusion_matrix(df['actual_breed'], df['predicted_breed'])

        # Wizualizacja Confusion Matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                    xticklabels=sorted(unique_breeds),
                    yticklabels=sorted(unique_breeds))

        plt.xlabel('Wykryta rasa psa')
        plt.ylabel('Rzeczywista rasa psa')
        plt.title('Confusion Matrix dla aktualnie wybranego modelu')

        #plt.xticks(rotation=45, fontsize=10)  # Obrót etykiet osi X i zmniejszenie rozmiaru czcionki
        #plt.yticks(rotation=45, fontsize=10)  # Obrót etykiet osi Y i zmniejszenie rozmiaru czcionki
        plt.xticks(fontsize=8)  # Obrót etykiet osi X i zmniejszenie rozmiaru czcionki
        plt.yticks(fontsize=8)  # Obrót etykiet osi Y i zmniejszenie rozmiaru czcionki
        plt.subplots_adjust(left=0.2, bottom=0.25)  # Dostosowanie marginesów z lewej i u dołu

        # Zapisanie wykresu do bufora tymczasowego
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Wczytanie PixMap z bufora
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        pixmap = pixmap.scaled(self.ui.matrix_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Ustawienie PixMap w QLabel
        self.ui.matrix_label.setPixmap(pixmap)

        # Czyszczenie bufora i zamykanie plot
        buf.close()
        plt.close()


# Funkcje związane z obsługą modeli i przewidywaniem rasy psa
##################################################################################################################################################################################
    # Funkcja aktualizująca etykietę oraz nazwę tabeli dla wybranego modelu na podstawie wybranego modelu w ComboBoxie
    # Aktualizuje również Confusion Matrix
    def update_label_and_model(self):
        selected_model = self.ui.modelComboBox.currentText()
        # Ustawienie formatowania etykiety
        style = "color: white; font-weight: bold;"
        self.ui.selectedModelLabel.setStyleSheet(style)
        self.ui.selectedModelLabel.setText(f"{selected_model}")

        # Ustawienie aktualnie nazwy tabeli w bazie danych dla tego modelu
        if self.ui.modelComboBox.currentIndex() == 0:
            self.selected_model_table_name = "inception_matrix"
        elif self.ui.modelComboBox.currentIndex() == 1:
            self.selected_model_table_name = "own_inception_matrix"
        elif self.ui.modelComboBox.currentIndex() == 2:
            self.selected_model_table_name = "own_yolo_matrix"
        # Na koniec (aby niepotrzebnie nie blokować wyświetlania innych danych) aktualizuje Confusion Matrix
        self.generate_confusion_matrix()

    # Funkcja wywoływana po kliknięciu przycisku rozpoznawania rasy psa
    # Sprawdza, który model jest wybrany i wywołuje odpowiednią funkcję
    def on_detect_breed_button_clicked(self):
        index = self.ui.modelComboBox.currentIndex()

        # Sprawdź, czy lastly_uploaded_picture jest puste przed wywołaniem funkcji, aby upewnić się, że obraz został wczytany
        if self.lastly_uploaded_picture is None:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("NIE DODANO ZDJĘCIA")
            msg_box.setText("Proszę wczytać zdjęcie przed próbą uruchomienia rozpoznawania rasy psa.")
            msg_box.exec()
            return

        if index == 0:
            self.predict_dog_breed_inceptionV3(True)
        elif index == 1:
            self.predict_dog_breed_inceptionV3_own()
        elif index == 2:
            self.predict_dog_breed_yoloV8_own()

    # Funckja otwierająca eksplorator plików i wczytująca obraz do Labela uploadedPictureLabel
    def select_and_display_image(self, event):
        # Otwórz okno wyboru pliku
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.lastly_uploaded_picture = Image.open(file_path)
            # Wczytaj i przeskaluj obraz
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Wyświetl obraz
            self.ui.uploadedPictureLabel.setPixmap(pixmap)

    # Funkcja do przewidywania rasy psa na podstawie obrazu przy pomocy modelu InceptionV3
    # Przyjmuje parametr print_results, który określa, czy funkcja ma wyświetlić wynik w Labelu czy zwrócić go
    def predict_dog_breed_inceptionV3(self, print_results):
        try:
            img = self.lastly_uploaded_picture.resize((299, 299))
            img_array = image.img_to_array(img)

            img = np.expand_dims(img_array, axis=0)
            img = preprocess_input(img)

            predictions = self.inceptionv3_model.predict(img)
            decoded_predictions = decode_predictions(predictions, top=1)[0]
            predicted_breed = decoded_predictions[0][1]
            if print_results:
                # Sprawdzenie, czy przewidywany kod rasy znajduje się w zbiorze etykiet dla naszego własnego modelu InceptionV3
                # Robimy to, bo pretrenowany model InceptionV3 rozpoznaje więcej rzeczy niż tylko rasy psów
                if predicted_breed.lower() in self.dog_breeds_list:
                    self.ui.detectedBreedLabel.setText(f"{predicted_breed}")
                else:
                    self.ui.detectedBreedLabel.setText("Brak psa na zdjęciu")

                # Po wykonaniu predykcji wyświetl okno dialogowe z pytaniem, czy model rozpoznał rasę psa poprawnie
                self.show_confirmation_dialog()

            else:
                if predicted_breed.lower() in self.dog_breeds_list:
                    return predicted_breed.lower()
                else:
                    return "Brak psa na zdjęciu"
        except Exception as e:
            self.ui.detectedBreedLabel.setText(f"Błąd: {str(e)}")

    # Funkcja do przewidywania rasy psa na podstawie obrazu przy pomocy naszego własnego modelu InceptionV3
    def predict_dog_breed_inceptionV3_own(self):
        try:
            img = self.lastly_uploaded_picture.resize((299, 299))
            img_array = image.img_to_array(img)

            img = np.expand_dims(img_array, axis=0)
            img = preprocess_input(img)

            predictions = self.inceptionv3_own_model.predict(img)
            predicted_breed_index = np.argmax(predictions)
            # Użyj słownika labels do przemapowania indeksu na nazwę rasy
            predicted_breed_name = self.labels[str(predicted_breed_index)]

            self.ui.detectedBreedLabel.setText(f"{predicted_breed_name}")

            # Po wykonaniu predykcji wyświetl okno dialogowe z pytaniem, czy model rozpoznał rasę psa poprawnie
            self.show_confirmation_dialog()
        except Exception as e:
            self.ui.detectedBreedLabel.setText(f"Błąd: {str(e)}")

    def predict_dog_breed_yoloV8_own(self):
        try:
            results = self.yolov8_own_model.predict(self.lastly_uploaded_picture)
            result = results[0]

            # Wyświetla nazwę i zdjęcie wykrytej rasy psa, jeśli została wykryta
            if len(result.boxes) > 0:
                box = result.boxes[0]

                # Wyświetlanie obrazu z zaznaczonymi bounding boxami
                pixmap = self.array_to_qpixmap(result.plot()[:, :, ::-1])
                pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui.uploadedPictureLabel.setPixmap(pixmap)

                predicted_breed = result.names[box.cls[0].item()]
                self.ui.detectedBreedLabel.setText(f"{predicted_breed}")
            else:
                self.ui.detectedBreedLabel.setText("Brak psa na zdjęciu")

            # Po wykonaniu predykcji wyświetl okno dialogowe z pytaniem, czy model rozpoznał rasę psa poprawnie
            self.show_confirmation_dialog()
        except Exception as e:
            self.ui.detectedBreedLabel.setText(f"Błąd: {str(e)}")

# Funkcje związane z kamerą i robieniem zdjęcia
##################################################################################################################################################################################
    # Konwersja numpy array na QPixmap
    def array_to_qpixmap(self, array):
        img = Image.fromarray(array)
        img = img.convert("RGBA")
        data = img.tobytes("raw", "BGRA")
        qimage = QImage(data, img.size[0], img.size[1], QImage.Format_ARGB32)
        qpixmap = QPixmap.fromImage(qimage)
        return qpixmap

    @Slot()
    def open_camera(self):
        self.cameraWindow = CameraWindow(self)
        self.cameraWindow.show()

    def set_captured_image(self, pixmap, cv_img):
        """ Ustawia zrobione zdjęcie w QLabel oraz w zmiennej lastly_uploaded_picture"""
        if pixmap:
            self.ui.uploadedPictureLabel.setPixmap(pixmap)
            img = Image.fromarray(cv_img)
            self.lastly_uploaded_picture = img

# Funkcje związane z obsługą analizy otrzymanych wyników
##################################################################################################################################################################################
    # Funkcja wyświetlająca okno dialogowe, w którym decydujemy czy model rozpoznał rasę psa poprawnie
    # Na początku wykrywa rasę psa przy pomocy najlepszego modelu InceptionV3, aby dać wskazówkę użytkownikowi czy inny model się pomylił
    def show_confirmation_dialog(self):
        proposed_actual_breed = self.predict_dog_breed_inceptionV3(False)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Walidacja wyniku")
        msg_box.setText("Czy rasa psa rozpoznana przez model zgadza się z prawdziwą rasą psa? \n \n Rasa psa zwrócona przez aktualnie wybrany model: " + self.ui.detectedBreedLabel.text().lower() + "\n\n Rzeczywista rasa psa proponowana przez pretrenowany model InceptionV3: " + proposed_actual_breed + "\n")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Ustawienie niestandardowych etykiet dla przycisków
        msg_box.setButtonText(QMessageBox.Yes, "Tak")
        msg_box.setButtonText(QMessageBox.No, "Nie")

        result = msg_box.exec()

        if result == QMessageBox.Yes:
            self.result_valid()
        elif result == QMessageBox.No:
            self.result_invalid(proposed_actual_breed)

    # Funkcja dodająca do bazy danych wynik dla prawidłowo rozpoznanej rasy psa (dwie takie same wartości)
    # Wszystkie litery w nazwie rasy psa są małe, aby uniknąc problemów z wielkością liter w różnych modelach
    def result_valid(self):
        self.db_connector.insert_result_record(self.selected_model_table_name, self.ui.detectedBreedLabel.text().lower(), self.ui.detectedBreedLabel.text().lower())

    def result_invalid(self, proposed_actual_breed):
        self.show_dialog(proposed_actual_breed)
        
    # Funkcja wyświetlająca okno dialogowe w przypadku, gdy model rozpoznał rasę psa niepoprawnie
    # Przekazuje do okna dialogowego nazwę rasy psa rozpoznanej przez model, listę ras psów, aby można było wybrać poprawną rasę psa
    # Oraz nazwę tabeli w bazie danych dla aktualnie wybranego modelu i obiekt klasy DatabaseConnector
    def show_dialog(self, proposed_actual_breed):
        predicted_breed = self.ui.detectedBreedLabel.text().lower()
        dialog = self.DogInfoDialog(predicted_breed, proposed_actual_breed, self.dog_breeds_list, self.selected_model_table_name, self.db_connector)
        dialog.exec()

    # Subklasa okna dialogowego, które pojawia się po kliknięciu przycisku Nie w oknie dialogowym z pytaniem o poprawność predykcji
    class DogInfoDialog(QDialog):
        def __init__(self, predicted_breed, proposed_actual_breed, dog_breeds_list, selected_model_table_name, db_connector, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Wprowadź poprawną rasę psa, jeśli model się pomylił")

            self.layout = QVBoxLayout()

            self.detected_label = QLabel(f"Rasa psa zwrócona przez aktualnie wybrany model: {predicted_breed}")
            self.layout.addWidget(self.detected_label)

            self.detected_label = QLabel(f"Rzeczywista rasa psa proponowana przez pretrenowany model InceptionV3:: {proposed_actual_breed}")
            self.layout.addWidget(self.detected_label)

            self.actual_breed_label = QLabel("Rzeczywista rasa psa: ")
            self.layout.addWidget(self.actual_breed_label)

            self.actual_breed_combo = QComboBox()
            self.actual_breed_combo.addItem("Brak psa na zdjęciu")
            self.actual_breed_combo.addItems(dog_breeds_list)  # Dodaj wszystkie elementy z listy dog_breeds_list do ComboBoxa
            self.layout.addWidget(self.actual_breed_combo)

            self.next_button = QPushButton("Zatwierdź")
            self.next_button.clicked.connect(lambda: self.on_button_clicked(predicted_breed, selected_model_table_name))
            self.layout.addWidget(self.next_button)

            self.setLayout(self.layout)

        # Funkcja wywoływana po kliknięciu przycisku Zatwierdź w oknie dialogowym
        # Dodaje do bazy danych wynik dla nieprawidłowo rozpoznanej rasy psa
        def on_button_clicked(self, predicted_breed, selected_model_table_name):
            selected_breed = self.actual_breed_combo.currentText().lower()
            db_connector.insert_result_record(selected_model_table_name, predicted_breed, selected_breed)
            self.accept()

# MAIN
##################################################################################################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_connector = DatabaseConnector()
    window = MainWindow(db_connector)
    sys.exit(app.exec())