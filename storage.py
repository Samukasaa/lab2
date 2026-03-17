# storage.py
import os
from parser import MenuParser

class FileStorage:
    """Класс для управления файлами."""

    def __init__(self, filename: str = "data.txt"):
        self.filename = filename

    def load_all(self) -> list:
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
        with open(self.filename, "w", encoding="utf-8") as f:
            for item in items:
                f.write(item.to_string() + "\n")