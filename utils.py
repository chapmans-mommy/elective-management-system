from datetime import date


def input_int(prompt: str) -> int:

    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> date:

    while True:
        try:
            return date.fromisoformat(input(prompt))
        except ValueError:
            print("Ошибка: введите дату в формате ГГГГ-ММ-ДД.")
