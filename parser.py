# parser.py
import re
from models import MenuItem

class MenuParser:
    """Класс для парсинга строк."""

    @staticmethod
    def parse_line(line: str) -> MenuItem:
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