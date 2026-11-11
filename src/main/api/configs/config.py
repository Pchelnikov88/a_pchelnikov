from pathlib import Path
from typing import Any


"""Config — это класс для хранения и чтения конфигурации (настроек) проекта. 
Он реализует паттерн Singleton (Одиночка), что значит, 
что в программе всегда существует только один экземпляр этого класса.

Вот что он делает и зачем нужен:
Без Config пришлось бы хардкодить адрес сервера в каждом тесте или реквестере:
"""
class Config:
    _instance = None
    _dictionary = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)

            config_path = Path(__file__).parents[4] / 'resources' / 'urls.properties'

            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found: {config_path}")

            with open(config_path, "r") as f:
                for line in f:
                    if "=" in line:
                        # maxsplit=1 нужен, чтобы знаки '=' внутри значения (если появятся) не ломали парсинг
                        key, value = line.split("=", 1)
                        # .strip() убирает невидимые символы переноса строки (\n) и пробелы по краям
                        cls._dictionary[key.strip()] = value.strip()

        return cls._instance

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        return Config()._dictionary.get(key, default_value)