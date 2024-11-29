from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import QFile, QTextStream

class AboutDialog(QDialog):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("О программе")

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # Кнопка для закрытия диалога
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.accept)  # Закрывает диалог при нажатии
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        # Загрузка текста из файла
        self.load_text(file_path)

    def load_text(self, file_path):
        file = QFile(file_path)
        if file.open(QFile.OpenModeFlag.ReadOnly):
            text_stream = QTextStream(file)
            self.text_edit.setPlainText(text_stream.readAll())
            file.close()  # Закрываем файл после чтения
        else:
            self.text_edit.setPlainText("Не удалось открыть файл.")
