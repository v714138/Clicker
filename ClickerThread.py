import time

import pyautogui
from PyQt6.QtCore import QThread


class ClickerThread(QThread):
    def __init__(self, click_type=1, mouse_button=1, interval=10, x=0, y=0):
        super().__init__()
        self.running = False
        self.interval = interval
        self.click_type = click_type
        self.mouse_button = mouse_button
        self.x = x
        self.y = y
        pyautogui.FAILSAFE = False

    def click(self):
        print('клик', self.x, self.y)
        # Определение типа клика
        if self.mouse_button == 1:  # Левая кнопка
            if self.click_type == 1:  # Одинарный клик
                pyautogui.click(self.x, self.y)
            elif self.click_type == 2:  # Двойной клик
                pyautogui.doubleClick(self.x, self.y)
        elif self.mouse_button == 2:  # Правая кнопка
            if self.click_type == 1:  # Одинарный клик
                pyautogui.click(self.x, self.y, button='right')
            elif self.click_type == 2:  # Двойной клик
                pyautogui.doubleClick(self.x, self.y, button='right')

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def run(self):
        while self.running:
            time.sleep(self.interval)
            if self.running:
                self.click()


    def start_clicking(self):
        self.running = True
        self.start()

    def stop_clicking(self):
        self.running = False