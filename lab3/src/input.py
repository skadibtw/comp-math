from typing import Any, Callable

from parse import parse_int, parse_float


# Вспомогательная функция для проверки, является ли значение целым числом или числом с плавающей точкой.
def _is_float_or_int(n: Any) -> bool:
    """Проверяет, является ли n float или int."""
    return isinstance(n, int) or isinstance(n, float)


# Читает число с плавающей точкой из стандартного ввода, повторяя запрос до получения корректного значения.
# message: Сообщение для пользователя.
# checker: Опциональная функция для дополнительной проверки введенного значения.
def read_float_from_stdin(message: str, checker: Callable[[float], bool] = lambda x: True) -> float:
    """Читает float из stdin."""
    f = None
    while not f:
        print(f'{message}')
        f = parse_float(input())

        if f is not None and checker(f):
            break
        else:
            f = None

    return f


# Читает целое число из стандартного ввода, повторяя запрос до получения корректного значения.
# message: Сообщение для пользователя.
# checker: Опциональная функция для дополнительной проверке введенного значения.
def read_int_from_stdin(message: str, checker: Callable[[int], bool] = lambda x: True) -> int:
    """Читает int из stdin."""
    f = None
    while not f:
        print(f'{message}')
        f = parse_int(input())

        if f is not None and checker(f):
            break
        else:
            f = None

    return f


# Предлагает пользователю выбрать один из вариантов из списка.
# message: Сообщение для пользователя.
# choices: Список вариантов для выбора.
# Возвращает индекс выбранного элемента в списке.
def read_choice_from_stdin(message: str, choices: list[Any]) -> int:
    """Выбор из списка. Возвращает выбранный индекс."""
    choice_count = len(choices)

    s = f'{message} [1-{choice_count}]:'

    for i, choice in enumerate(choices):
        s += f'\n{i + 1}. {choice}'

    index = read_int_from_stdin(s, lambda n: 1 <= n <= choice_count)
    index -= 1

    return index
