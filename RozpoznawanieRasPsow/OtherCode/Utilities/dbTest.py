import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtWidgets import QLineEdit, QComboBox
import mysql.connector

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


class AddRecordWindow(QMainWindow):
    def __init__(self, db_connector):
        super().__init__()
        self.db_connector = db_connector
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Record to Statistics")
        self.setGeometry(100, 100, 300, 150)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.model_name_label = QLabel("Model Name:")
        self.model_name_input = QLineEdit()
        self.layout.addWidget(self.model_name_label)
        self.layout.addWidget(self.model_name_input)

        self.is_correct_label = QLabel("Is Correct (True/False):")
        self.is_correct_input = QComboBox()
        self.is_correct_input.addItems(["True", "False"])
        self.layout.addWidget(self.is_correct_label)
        self.layout.addWidget(self.is_correct_input)

        self.add_record_button = QPushButton("Add Record")
        self.add_record_button.clicked.connect(self.add_record)
        self.layout.addWidget(self.add_record_button)

        self.central_widget.setLayout(self.layout)


    def add_record(self):
        try:
            model_name = self.model_name_input.text()
            is_correct_text = self.is_correct_input.currentText()

            if model_name and is_correct_text in ("True", "False"):
                is_correct = is_correct_text == "True"
                self.db_connector.insert_record(model_name, is_correct)
                self.model_name_input.clear()
                self.is_correct_input.setCurrentIndex(0)
        except Exception as e:
            print(f"An error occurred: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    db_connector = DatabaseConnector()

    main_window = AddRecordWindow(db_connector)
    main_window.show()

    sys.exit(app.exec())
