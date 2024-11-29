from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from pynput import keyboard

from dialog_ui import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):

    def __init__(self, stop_key):
        super().__init__()
        # uic.loadUi("Main.ui", self)
        self.setupUi(self)
        self.setWindowTitle('Выбор горячей клавиши')
        self.key_map = {
            keyboard.Key.esc: "ESC",
            keyboard.Key.f1: "F1",
            keyboard.Key.f2: "F2",
            keyboard.Key.f3: "F3",
            keyboard.Key.f4: "F4",
            keyboard.Key.f5: "F5",
            keyboard.Key.f6: "F6",
            keyboard.Key.space: "SPACE",
            keyboard.Key.backspace: "BACKSPACE",
            keyboard.Key.tab: "TAB",
            keyboard.Key.enter: "ENTER",
            keyboard.Key.delete: "DELETE",
            keyboard.Key.home: "HOME",
            keyboard.Key.end: "END",
            keyboard.Key.left: "LEFT",
            keyboard.Key.right: "RIGHT",
            keyboard.Key.up: "UP",
            keyboard.Key.down: "DOWN",
        }
        self.stop_key = stop_key
        self.lineEdit.setText(self.key_map.get(stop_key, stop_key))
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

    def on_key_press(self, key):
        print(key)
        if key in self.key_map:
            key_text = self.key_map[key]
            self.lineEdit.setText(key_text)
            self.stop_key = key
