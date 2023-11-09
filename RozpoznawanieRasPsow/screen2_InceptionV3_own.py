# screen2.py

import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from keras.preprocessing import image

class Screen2(QWidget):
    # Wczytaj swój model z pliku inception_model.h5
    custom_model = load_model('C:/Users/micha/OneDrive/Pulpit/AI/model_inception.h5')

    # Załaduj pre-trenowany model InceptionV3
    model = InceptionV3(weights='imagenet')
    def __init__(self):
        super().__init__()
        self.camera = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rozpoznawanie rasy psa - Ekran 2')

        # Layout
        layout = QVBoxLayout()

        # Przyciski
        self.btn_layout = QHBoxLayout()
        self.btn_choose_image = QPushButton('Wybierz zdjęcie', self)
        self.btn_choose_image.clicked.connect(self.chooseImage)
        self.btn_layout.addWidget(self.btn_choose_image)

        self.btn_open_camera = QPushButton('Otwórz kamerę', self)
        self.btn_open_camera.clicked.connect(self.toggleCameraView)
        self.btn_layout.addWidget(self.btn_open_camera)

        layout.addLayout(self.btn_layout)

        # Widok kamery
        self.camera_view = QLabel(self)
        self.camera_view.hide()  # domyślnie ukryty

        self.btn_capture = QPushButton('Zrób zdjęcie', self)
        self.btn_capture.hide()  # domyślnie ukryty
        self.btn_capture.clicked.connect(self.captureImage)

        layout.addWidget(self.camera_view)
        layout.addWidget(self.btn_capture)

        # Etykieta do wyświetlenia zdjęcia
        self.label_image = QLabel(self)
        self.label_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_image)

        # Etykieta do wyświetlenia rasy psa
        self.label_prediction = QLabel('Rasa: Nieznana', self)
        self.label_prediction.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_prediction)

        self.setLayout(layout)

    def chooseImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Wybierz zdjęcie', filter="Images (*.png *.xpm *.jpg)")

        if fname:
            # Wyświetl wybrane zdjęcie
            pixmap = QPixmap(fname)
            self.label_image.setPixmap(pixmap.scaled(224, 224, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # przeskaluj do 224x224

            # Przetwarzanie i przewidywanie rasy
            try:
                img = image.load_img(fname, target_size=(224, 224))
                img_array = image.img_to_array(img)
                predicted_breed = self.predict_dog_breed(img_array)
                self.label_prediction.setText(f"Rasa: {predicted_breed}")
            except Exception as e:
                self.label_prediction.setText(f"Błąd: {str(e)}")

    def initCamera(self):
        if not self.camera:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                self.label_prediction.setText("Nie można połączyć z kamerą")
                return False

            self.timer = QTimer()
            self.timer.timeout.connect(self.updateFrame)
            self.timer.start(100)  # Odświeżaj co 100ms
        return True

    def toggleCameraView(self):
        if self.camera_view.isHidden():
            if self.initCamera():
                self.camera_view.show()
                self.btn_capture.show()
                self.btn_open_camera.setText('Zamknij kamerę')
        else:
            self.hideCameraView()

    def hideCameraView(self):
        self.camera_view.hide()
        self.btn_capture.hide()
        self.btn_open_camera.setText('Otwórz kamerę')
        if self.camera:
            self.timer.stop()
            self.camera.release()
            self.camera = None

    def updateFrame(self):
        ret, frame = self.camera.read()
        if ret:
            self.camera_view.setPixmap(self.convert_cv_qt(frame))

    def captureImage(self):
        ret, frame = self.camera.read()
        if ret:
            self.hideCameraView()
            pixmap = self.convert_cv_qt(frame)
            self.label_image.setPixmap(pixmap.scaled(224, 224, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # przeskaluj do 224x224

            # Przetwarzanie i przewidywanie rasy
            try:
                frame_resized = cv2.resize(frame, (224, 224))  # zmień rozmiar na 224x224 dla modelu
                img_array = image.img_to_array(frame_resized)
                predicted_breed = self.predict_dog_breed(img_array)
                self.label_prediction.setText(f"Rasa: {predicted_breed}")
            except Exception as e:
                self.label_prediction.setText(f"Błąd: {str(e)}")

    def predict_dog_breed(self, img_array):
        img = np.expand_dims(img_array, axis=0)
        img = preprocess_input(img)

        predictions = custom_model.predict(img)
        predicted_breed_index = np.argmax(predictions)
        predicted_breed_name = labels[str(predicted_breed_index)]
        return predicted_breed_name

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
