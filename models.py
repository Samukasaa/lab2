# models.py
class MenuItem:
    """Класс модели данных для блюда меню."""

    def __init__(self, obj_type: str, name: str, price: float, cook_time: str):
        self.obj_type = obj_type
        self.name = name
        self.price = price
        self.cook_time = cook_time

    def to_string(self) -> str:
        return f'{self.obj_type} "{self.name}" {self.price} {self.cook_time}'

    def to_tuple(self) -> tuple:
        return (self.obj_type, self.name, str(self.price), self.cook_time)