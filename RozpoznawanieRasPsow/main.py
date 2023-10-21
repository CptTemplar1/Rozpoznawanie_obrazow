# -*- coding: utf-8 -*-

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from keras.preprocessing import image

# Załaduj pre-trenowany model InceptionV3
model = InceptionV3(weights='imagenet')

# Funkcja do przewidywania rasy psa na podstawie obrazu
def predict_dog_breed(image_path):
    img = image.load_img(image_path, target_size=(299, 299))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    predictions = model.predict(img)
    decoded_predictions = decode_predictions(predictions, top=1)[0]

    return decoded_predictions[0][1]

class DogBreedIdentifierApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rozpoznawanie rasy psa')

        # Layout
        layout = QVBoxLayout()

        # Przycisk do wyboru zdjęcia
        self.btn_choose_image = QPushButton('Wybierz zdjęcie', self)
        self.btn_choose_image.clicked.connect(self.chooseImage)
        layout.addWidget(self.btn_choose_image)

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
        fname = QFileDialog.getOpenFileName(self, 'Wybierz zdjęcie', filter="Images (*.png *.xpm *.jpg)")[0]

        if fname:
            # Wyświetl wybrane zdjęcie
            pixmap = QPixmap(fname)
            self.label_image.setPixmap(pixmap.scaled(self.label_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            try:
                # Użyj AI do przewidzenia rasy psa
                predicted_breed = predict_dog_breed(fname)
                self.label_prediction.setText(f"Rasa: {predicted_breed}")
            except Exception as e:
                self.label_prediction.setText(f"Błąd: {str(e)}")

def main():
    app = QApplication(sys.argv)
    ex = DogBreedIdentifierApp()
    ex.resize(600, 600)  # Możesz dostosować rozmiar okna aplikacji
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
