import sys

from PyQt6.QtGui import QFontMetrics
from pynput import mouse, keyboard
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication

from Clicker import Ui_MainWindow
from ClickerThread import ClickerThread
from about import AboutDialog
from database import Database
from dialog import Dialog


def adjust_button_size(button):
    metrics = QFontMetrics(button.font())
    text_width = metrics.horizontalAdvance(button.text())
    button.setFixedWidth(text_width + 20)


class Clicker(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi("Clicker.ui", self)
        self.setupUi(self)
        self.setWindowTitle('Кликер')
        self.stop_key = keyboard.Key.f6
        self.showDialog.clicked.connect(self.open_dialog)
        self.start.clicked.connect(self.start_clicking)
        self.x, self.y = 100, 100
        self.x_position.setDisabled(True)
        self.y_position.setDisabled(True)
        self.current_location.setChecked(True)
        self.current_location.toggled.connect(self.change_location)
        self.select_location.toggled.connect(self.change_location)
        # self.x_position.setEnabled(False)
        self.hours.setText('0')
        self.minutes.setText('0')
        self.seconds.setText('0')
        self.milliseconds.setText('0')

        self.check_click = False
        self.pick_coord.clicked.connect(self.start_listening)
        self.stop.clicked.connect(self.stop_clicking)

        # комбобоксы
        self.type_clicks = {1: "Одинарный", 2: "Двойной"}
        self.type_click.addItems(self.type_clicks.values())
        self.mouse_buttons = {1: "Левая", 2: "Правая"}
        self.mouse_button.addItems(self.mouse_buttons.values())

        # Инициализация слушателя клавиатуры и мыши
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

        self.stop.setEnabled(False)
        adjust_button_size(self.pick_coord)
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.mouse_listener.start()
        self.clicker_thread = ClickerThread()

        # Кнопки меню: Файл, Справка
        self.save.triggered.connect(self.save_config)
        self.open.triggered.connect(self.open_config)
        self.about.triggered.connect(self.open_about)

        # объект базы данных
        self.db = Database('./clicker.db')

    def open_about(self):
        dialog = AboutDialog('about.txt')
        dialog.exec()

    def save_config(self):
        result = self.db.save_config(
            int(self.hours.text()),
            int(self.minutes.text()),
            int(self.seconds.text()),
            int(self.milliseconds.text()),
            self.x,
            self.y,
            int(self.current_location.isChecked()),
            self.type_click.currentIndex() + 1,
            self.mouse_button.currentIndex() + 1
        )
        print(result)

    def open_config(self):
        res = self.db.open_config()
        _, hours, minutes, seconds, milliseconds, x, y, current_location, type_click, mouse_button = res
        print(hours, minutes, seconds, milliseconds, x, y, current_location, type_click, mouse_button)
        self.hours.setText(str(hours))
        self.minutes.setText(str(minutes))
        self.seconds.setText(str(seconds))
        self.milliseconds.setText(str(milliseconds))
        self.x = x
        self.y = y
        self.x_position.setText(str(self.x))
        self.y_position.setText(str(self.y))
        if current_location:
            self.current_location.setChecked(True)
        else:
            self.select_location.setChecked(True)
        self.type_click.setCurrentIndex(type_click - 1)
        self.mouse_button.setCurrentIndex(mouse_button - 1)

    def change_location(self):
        if self.current_location.isChecked():
            self.x_position.setDisabled(True)
            self.y_position.setDisabled(True)
            self.pick_coord.setDisabled(True)
        elif self.select_location.isChecked():
            self.x_position.setDisabled(False)
            self.y_position.setDisabled(False)
            self.pick_coord.setDisabled(False)

    def start_listening(self):
        self.check_click = True

    def on_click(self, x, y, button, pressed):
        if pressed and self.check_click:
            self.x = x
            self.y = y
            self.x_position.setText(str(self.x))
            self.y_position.setText(str(self.y))
            print(f"Нажата мышь в ({x}, {y}) с кнопкой {button}")
            self.check_click = False

    def start_clicking(self):

        hours = int(self.hours.text())
        minutes = int(self.minutes.text())
        seconds = int(self.seconds.text())
        milliseconds = int(self.milliseconds.text())

        total_time = (hours * 3600 + minutes * 60 + seconds) + milliseconds / 1000

        if total_time > 0:
            self.stop.setEnabled(True)
            self.start.setEnabled(False)
            click_type = self.type_click.currentIndex() + 1
            mouse_button = self.mouse_button.currentIndex() + 1
            self.clicker_thread = ClickerThread(
                click_type, mouse_button, total_time, self.x, self.y
            )
            self.clicker_thread.start_clicking()
            self.statusBar().showMessage(f'Таймер запущен, клики будут происходить каждые {total_time} с')
        else:
            self.statusBar().showMessage('Пожалуйста, введите положительное время.')

    def on_move(self, x, y):
        if self.current_location.isChecked() and self.clicker_thread.running:
            self.x = x
            self.y = y
            self.x_position.setText(str(self.x))
            self.y_position.setText(str(self.y))
            print(f"Курсор перемещен в ({x}, {y})")
            self.clicker_thread.set_coords(x, y)

    def open_dialog(self):
        dialog = Dialog(self.stop_key)
        is_ok = dialog.exec()
        if is_ok:
            self.stop_key = dialog.stop_key

    def on_key_press(self, key):
        try:
            if key == self.stop_key:
                self.stop_clicking()
        except Exception as e:
            print(f"Ошибка: {e}")

    def stop_clicking(self):
        self.clicker_thread.stop_clicking()
        print('Клики остановлены.')
        self.stop.setEnabled(False)
        self.start.setEnabled(True)

    def closeEvent(self, event):
        self.listener.stop()
        self.mouse_listener.stop()
        event.accept()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    from PyQt6 import QtCore, QtWidgets

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ex = Clicker()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
