

import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
import sys


# ------------------------------------------------------------------------------
# Модуль данных (Data Model)
# ------------------------------------------------------------------------------

class MenuItem:
    """Класс модели данных для блюда меню."""

    def __init__(self, obj_type: str, name: str, price: float, cook_time: str):
        self.obj_type = obj_type
        self.name = name
        self.price = price
        self.cook_time = cook_time

    def to_string(self) -> str:
        """Сериализует объект в строку для записи в файл."""
        return f'{self.obj_type} "{self.name}" {self.price} {self.cook_time}'

    def to_tuple(self) -> tuple:
        """Возвращает кортеж данных для отображения в таблице."""
        return (self.obj_type, self.name, str(self.price), self.cook_time)


# ------------------------------------------------------------------------------
# Модуль парсинга (Parser Logic)
# ------------------------------------------------------------------------------

class MenuParser:
    """Класс, отвечающий за парсинг строк в объекты (SRP: Парсинг)."""

    @staticmethod
    def parse_line(line: str) -> MenuItem:
        """
        Разбирает одну строку файла и возвращает объект MenuItem.
        Обновленный шаблон поддерживает кириллицу в типе объекта.
        """
        # [\wа-яА-ЯёЁ]+ разрешает русские буквы в первом слове (Типе)
        pattern = r'^([\wа-яА-ЯёЁ]+)\s+"([^"]+)"\s+([\d.]+)\s+(\d{2}:\d{2})$'
        match = re.match(pattern, line.strip())

        if not match:
            raise ValueError(f"Некорректная строка: {line}")

        return MenuItem(
            obj_type=match.group(1),
            name=match.group(2),
            price=float(match.group(3)),
            cook_time=match.group(4)
        )


# ------------------------------------------------------------------------------
# Модуль работы с файлами (Storage Logic)
# ------------------------------------------------------------------------------

class FileStorage:
    """Класс для управления сохранением и загрузкой данных (SRP: Хранение)."""

    def __init__(self, filename: str = "data.txt"):
        self.filename = filename

    def load_all(self) -> list:
        """Считывает все объекты из файла в список."""
        items = []
        if not os.path.exists(self.filename):
            return items

        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        items.append(MenuParser.parse_line(line))
                    except ValueError:
                        continue
        return items

    def save_all(self, items: list):
        """Записывает список объектов в файл (перезапись)."""
        with open(self.filename, "w", encoding="utf-8") as f:
            for item in items:
                f.write(item.to_string() + "\n")


# ------------------------------------------------------------------------------
# Модуль интерфейса (GUI Logic)
# ------------------------------------------------------------------------------

class Application(tk.Tk):
    """Основное окно приложения (SRP: Интерфейс)."""

    def __init__(self):
        super().__init__()
        self.title("Меню Ресторана - На берегу")
        self.geometry("650x450")

        # Строка с ошибкой удалена - в Python 3 UTF-8 работает по умолчанию

        self.storage = FileStorage()
        self.items = []

        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        """Создает элементы интерфейса."""
        # Таблица
        columns = ("type", "name", "price", "time")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("type", text="Тип")
        self.tree.heading("name", text="Название")
        self.tree.heading("price", text="Цена")
        self.tree.heading("time", text="Время")

        self.tree.column("type", width=100)
        self.tree.column("name", width=300)
        self.tree.column("price", width=80)
        self.tree.column("time", width=80)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Панель управления
        control_frame = tk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(control_frame, text="Тип:").pack(side=tk.LEFT)
        self.entry_type = tk.Entry(control_frame, width=15)
        self.entry_type.pack(side=tk.LEFT, padx=5)
        self.entry_type.insert(0, "Меню")  # Значение по умолчанию на русском

        tk.Label(control_frame, text="Название:").pack(side=tk.LEFT)
        self.entry_name = tk.Entry(control_frame, width=25)
        self.entry_name.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Цена:").pack(side=tk.LEFT)
        self.entry_price = tk.Entry(control_frame, width=10)
        self.entry_price.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Время (ЧЧ:ММ):").pack(side=tk.LEFT)
        self.entry_time = tk.Entry(control_frame, width=10)
        self.entry_time.pack(side=tk.LEFT, padx=5)

        # Кнопки
        btn_add = tk.Button(control_frame, text="Добавить", command=self._add_item)
        btn_add.pack(side=tk.LEFT, padx=10)

        btn_del = tk.Button(control_frame, text="Удалить", command=self._delete_item)
        btn_del.pack(side=tk.LEFT)

    def _load_data(self):
        """Загружает данные из файла и обновляет таблицу."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.items = self.storage.load_all()

        for item in self.items:
            self.tree.insert("", tk.END, values=item.to_tuple())

    def _add_item(self):
        """Обработчик кнопки добавления."""
        t = self.entry_type.get()
        n = self.entry_name.get()
        p = self.entry_price.get()
        tm = self.entry_time.get()

        # Формируем строку для парсера
        test_string = f'{t} "{n}" {p} {tm}'

        try:
            new_item = MenuParser.parse_line(test_string)
            self.items.append(new_item)
            self.storage.save_all(self.items)
            self._load_data()
            messagebox.showinfo("Успех", "Объект добавлен")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def _delete_item(self):
        """Обработчик кнопки удаления."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите объект в таблице")
            return

        indices = [self.tree.index(item) for item in selected]
        indices.sort(reverse=True)

        for index in indices:
            del self.items[index]

        self.storage.save_all(self.items)
        self._load_data()


if __name__ == "__main__":
    app = Application()
    app.mainloop()