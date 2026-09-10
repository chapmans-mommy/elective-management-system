import json
import os


def load_data(filename: str) -> list:

    if not os.path.exists(filename):
        print(f"Файл {filename} не найден. Будет создан новый.")
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Ошибка чтения {filename}: файл повреждён.")
        return []
    except OSError as error:
        print(f"Ошибка доступа к {filename}: {error}")
        return []


def save_data(filename: str, data: list) -> None:

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")
