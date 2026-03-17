import tkinter as tk
from tkinter import messagebox
from help import HelpWindow
from gui_work import WorkWindow

class MainMenu(tk.Tk):
    """Главное меню программы."""

    def __init__(self):
        super().__init__()
        self.title("Главное меню - Ресторан")
        self.geometry("400x350")
        self.resizable(False, False)
        self._create_menu()

    def _create_menu(self):
        title_label = tk.Label(
            self,
            text="🍽️ РЕСТОРАН \"НА БЕРЕГУ\"",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        btn_work = tk.Button(
            button_frame,
            text="🔧 РАБОТАТЬ",
            command=self._open_work_window,
            width=28, height=2,
            font=("Arial", 11),
            bg="#4CAF50", fg="white"
        )
        btn_work.pack(pady=8)

        btn_help = tk.Button(
            button_frame,
            text="📖 СПРАВКА",
            command=self._open_help_window,
            width=28, height=2,
            font=("Arial", 11),
            bg="#2196F3", fg="white"
        )
        btn_help.pack(pady=8)

        btn_exit = tk.Button(
            button_frame,
            text="🚪 ВЫХОД",
            command=self._exit_app,
            width=28, height=2,
            font=("Arial", 11),
            bg="#f44336", fg="white"
        )
        btn_exit.pack(pady=8)

        footer_label = tk.Label(
            self,
            text="Разработчик: Васильев В.С.",
            font=("Arial", 9), fg="gray"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def _open_work_window(self):
        """Открывает рабочее окно."""
        self.withdraw()
        work_window = WorkWindow(self)

    def _open_help_window(self):
        """Открывает окно справки."""
        self.withdraw()
        help_window = HelpWindow(self)

    def _show_main_menu(self):
        """Показывает главное меню."""
        self.deiconify()

    def _exit_app(self):
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.destroy()