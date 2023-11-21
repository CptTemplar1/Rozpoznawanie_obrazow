import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtWidgets import QLineEdit, QComboBox
import mysql.connector

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

class DatabaseConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="RozpoznawanieRasPsow"
        )
        self.cursor = self.connection.cursor()

    def insert_record(self, modelName, isCorrect):
        query = "INSERT INTO Statistics (modelName, isCorrect) VALUES (%s, %s)"
        values = (modelName, isCorrect)
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_breed_record(self, predicted_breed, actual_breed):
        query = "INSERT INTO test_matrix (predicted_breed, actual_breed) VALUES (%s, %s)"
        values = (predicted_breed, actual_breed)
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_all_breeds(self):
        query = "SELECT predicted_breed, actual_breed FROM test_matrix"
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class MainWindow():
    def __init__(self, db_connector):
        super().__init__()
        self.db_connector = db_connector
        self.init_ui()

    def init_ui(self):

        for i in range(0, 5):
            self.db_connector.insert_breed_record("golden_retriever", "golden_retriever")

        # Pobranie danych z bazy danych
        data = self.db_connector.get_all_breeds()
        df = pd.DataFrame(data, columns=['predicted_breed', 'actual_breed'])

        # Tworzenie Confusion Matrix
        conf_matrix = confusion_matrix(df['actual_breed'], df['predicted_breed'])

        # Wizualizacja Confusion Matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(df['predicted_breed']),
                    yticklabels=np.unique(df['actual_breed']))
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    db_connector = DatabaseConnector()

    main_window = MainWindow(db_connector)

    sys.exit(app.exec())
