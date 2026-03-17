import tkinter as tk
from tkinter import ttk, messagebox
from storage import FileStorage


class WorkWindow(tk.Toplevel):
    """Рабочее окно с таблицей."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Управление меню")
        self.geometry("700x550")
        self.resizable(False, False)

        self.storage = FileStorage()
        self.items = []

        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        title_label = tk.Label(
            self, text="📋 МЕНЮ",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)

        columns = ("type", "name", "price", "time")
        self.tree = ttk.Treeview(
            self, columns=columns,
            show="headings", height=12
        )

        self.tree.heading("type", text="Тип")
        self.tree.heading("name", text="Название")
        self.tree.heading("price", text="Цена")
        self.tree.heading("time", text="Время")

        self.tree.column("type", width=100)
        self.tree.column("name", width=300)
        self.tree.column("price", width=80)
        self.tree.column("time", width=80)

        self.tree.pack(padx=10, pady=5)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Тип:").pack(side=tk.LEFT, padx=5)
        self.entry_type = tk.Entry(input_frame, width=12)
        self.entry_type.pack(side=tk.LEFT, padx=5)
        self.entry_type.insert(0, "Меню")

        tk.Label(input_frame, text="Название:").pack(side=tk.LEFT, padx=5)
        self.entry_name = tk.Entry(input_frame, width=25)
        self.entry_name.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="Цена:").pack(side=tk.LEFT, padx=5)
        self.entry_price = tk.Entry(input_frame, width=8)
        self.entry_price.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="Время:").pack(side=tk.LEFT, padx=5)
        self.entry_time = tk.Entry(input_frame, width=8)
        self.entry_time.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Добавить",
                  command=self._add_item, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Удалить",
                  command=self._delete_item, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="💾 Сохранить",
                  command=self._save_data, width=12).pack(side=tk.LEFT, padx=5)

        # Панель кнопок НАЗАД и ВЫХОД
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)

        btn_back = tk.Button(
            nav_frame,
            text="🔙 НАЗАД В МЕНЮ",
            command=self._go_back,
            width=25,
            height=2,
            bg="#FF9800",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2"
        )
        btn_back.pack(side=tk.LEFT, padx=10)

        btn_exit = tk.Button(
            nav_frame,
            text="🚪 ВЫХОД",
            command=self._exit_app,
            width=15,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Arial", 11),
            cursor="hand2"
        )
        btn_exit.pack(side=tk.LEFT, padx=10)

        self.status_var = tk.StringVar()
        status_bar = tk.Label(
            self, textvariable=self.status_var,
            bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.items = self.storage.load_all()

        for item in self.items:
            self.tree.insert("", tk.END, values=item.to_tuple())

        self.status_var.set(f"Загружено: {len(self.items)} блюд")

    def _add_item(self):
        from parser import MenuParser

        t = self.entry_type.get()
        n = self.entry_name.get()
        p = self.entry_price.get()
        tm = self.entry_time.get()

        test_string = f'{t} "{n}" {p} {tm}'

        try:
            new_item = MenuParser.parse_line(test_string)
            self.items.append(new_item)
            self.storage.save_all(self.items)
            self._load_data()
            messagebox.showinfo("Успех", "Блюдо добавлено!")

            self.entry_name.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_time.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def _delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите блюдо")
            return

        if messagebox.askyesno("Подтверждение", "Удалить?"):
            indices = [self.tree.index(item) for item in selected]
            indices.sort(reverse=True)

            for index in indices:
                del self.items[index]

            self.storage.save_all(self.items)
            self._load_data()

    def _save_data(self):
        try:
            self.storage.save_all(self.items)
            messagebox.showinfo("Сохранение", "Данные сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _go_back(self):
        """Возвращается в главное меню."""
        self.destroy()
        self.parent._show_main_menu()

    def _exit_app(self):
        """Закрывает программу."""
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.destroy()
            self.parent.destroy()