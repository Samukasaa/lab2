import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import os


class HelpWindow(tk.Toplevel):
    """Окно справки с прокруткой и кнопкой НАЗАД."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("📖 СПРАВКА - Ресторан \"На берегу\"")
        self.geometry("700x650")
        self.resizable(True, True)

        self._create_help_content()

    def _create_help_content(self):
        """Создает содержимое окна справки."""
        # Заголовок
        title_frame = tk.Frame(self, bg="#2196F3")
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="📖 СПРАВКА ПО ПРОГРАММЕ",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white",
            pady=15
        )
        title_label.pack()

        # 🖼️ КАРТИНКА
        try:
            if os.path.exists("logo.png"):
                img = Image.open("logo.png")
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)

                img_label = tk.Label(self, image=self.photo, bg="white")
                img_label.pack(pady=10)

                img_caption = tk.Label(
                    self,
                    text="Ресторан \"На берегу\"",
                    font=("Arial", 12, "italic"),
                    bg="white",
                    fg="#666666"
                )
                img_caption.pack(pady=5)
        except Exception as e:
            print(f"Не удалось загрузить картинку: {e}")

        # Панель кнопок
        btn_frame = tk.Frame(self, bg="#e0e0e0")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        # Кнопка НАЗАД
        btn_back = tk.Button(
            btn_frame,
            text="🔙 НАЗАД В МЕНЮ",
            command=self._go_back,
            width=25,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#FF9800",
            fg="white",
            cursor="hand2"
        )
        btn_back.pack(side=tk.LEFT, padx=10, pady=5)

        # Кнопка ВЫХОД
        btn_exit = tk.Button(
            btn_frame,
            text="🚪 ВЫХОД",
            command=self._exit_app,
            width=15,
            height=2,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        )
        btn_exit.pack(side=tk.LEFT, padx=10, pady=5)

        # Разделительная линия
        separator = tk.Frame(self, height=2, bg="#cccccc")
        separator.pack(fill=tk.X, padx=10, pady=5)

        # Прокручиваемая область
        text_frame = tk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg="white",
            padx=15,
            pady=15,
            spacing1=5,
            spacing3=5,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        help_text = """
📋 ОПИСАНИЕ ПРОГРАММЫ

Программа предназначена для управления меню ресторана. 
Позволяет добавлять, удалять и просматривать блюда.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔘 ГЛАВНОЕ МЕНЮ

При запуске программы отображается главное меню с тремя кнопками:

  🔧 РАБОТАТЬ
     Переход к окну управления меню ресторана.

  📖 СПРАВКА
     Открывает это окно с информацией о программе.

  🚪 ВЫХОД
     Закрывает программу (с подтверждением).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 РАБОЧЕЕ ОКНО (ТАБЛИЦА)

После нажатия кнопки "РАБОТАТЬ" открывается окно с таблицей.

Функции рабочего окна:

  ➕ Добавить
     Добавляет новое блюдо в меню.

  🗑️ Удалить
     Удаляет выбранное блюдо из таблицы.

  💾 Сохранить
     Сохраняет все изменения в файл data.txt.

  🔙 НАЗАД В МЕНЮ
     Возвращает в главное меню программы.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 ФОРМАТ ДАННЫХ

Каждое блюдо описывается следующими полями:

  Тип         Категория блюда
  Название    Наименование блюда (в кавычках)
  Цена        Стоимость в рублях
  Время       Время приготовления (ЧЧ:ММ)

Пример: Меню "Борщ" 150.50 00:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 ПОДСКАЗКИ

  • Данные сохраняются в файл data.txt
  • Время в 24-часовом формате
  • Для изменения размера окна перетащите границы

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👨‍ ИНФОРМАЦИЯ О РАЗРАБОТЧИКЕ

  Разработчик: Зацепина Т.А

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        self.text_area.insert(tk.END, help_text)
        self.text_area.config(state=tk.DISABLED)

        self.grab_set()

    def _go_back(self):
        """Возвращается в главное меню."""
        self.destroy()
        self.parent._show_main_menu()

    def _exit_app(self):
        """Закрывает программу."""
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.destroy()
            self.parent.destroy()