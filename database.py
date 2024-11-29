import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def save_config(
            self, hours,
            minutes,
            seconds,
            milliseconds,
            x,
            y,
            current_location,
            type_click,
            mouse_button
    ):
        try:
            print(hours,
            minutes,
            seconds,
            milliseconds,
            x,
            y,
            current_location,
            type_click,
            mouse_button)
            self.cursor.execute('''
                INSERT INTO config(
                hours, 
                minutes, 
                seconds, 
                milliseconds, 
                x, 
                y,
                current_location,
                type_click,
                mouse_button) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                hours,
                minutes,
                seconds,
                milliseconds,
                x,
                y,
                current_location,
                type_click,
                mouse_button
            ))
            self.connection.commit()
        except Exception as er:
            return f"Ошибка {er}"
        return "Конфигурация сохранена."

    def open_config(self):
        self.cursor.execute('SELECT * FROM config order by id desc')
        config = self.cursor.fetchone()
        return config

    def close(self):
        self.connection.close()
        print("Соединение с базой данных закрыто.")
