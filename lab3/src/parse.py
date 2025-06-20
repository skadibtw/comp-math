from typing import TypeVar, Callable

# Определение обобщенного типа T.
T = TypeVar('T')


# Кастомный конвертер строки в float, поддерживающий запятую в качестве десятичного разделителя.
def _float(s: str, *args, **kwargs) -> float:
    """Кастомный конвертер float."""
    return float(
        s.replace(',', '.'),
        *args,
        **kwargs,
    )


# Вспомогательная функция для парсинга числа (int или float) из строки.
# basic_parser: Функция для базового парсинга (int или _float).
# s: Входная строка.
# _min, _max: Опциональные границы для проверки значения.
# Возвращает число типа T или None в случае ошибки парсинга или выхода за границы.
def _parse_number(basic_parser: Callable[[str], T], s: str, _min: T = None, _max: T = None) -> T | None:
    """Парсит число."""
    s = s.strip().replace('_', '')

    number = None
    try:
        number = basic_parser(s)
    except ValueError:
        return None

    if _min and number < _min:
        return None

    if _max and number > _max:
        return None

    return number


# Парсит целое число из строки с опциональной проверкой границ.
def parse_int(s: str, _min: int = None, _max: int = None) -> int | None: # Добавлен None в тип возврата
    """Парсит int."""
    return _parse_number(int, s, _min, _max)


# Парсит число с плавающей точкой из строки с опциональной проверкой границ.
def parse_float(s: str, _min: float = None, _max: float = None) -> float | None: # Добавлен None в тип возврата
    """Парсит float."""
    return _parse_number(_float, s, _min, _max)


# Вспомогательная функция для парсинга строки чисел (int или float), разделенных пробелами.
# basic_parser: Функция для базового парсинга (int или _float).
# s: Входная строка.
# n: Ожидаемое количество чисел в строке.
# _min, _max: Опциональные границы для проверки каждого значения.
# Возвращает список чисел типа T или None в случае ошибки.
def _parse_number_row(basic_parser: Callable[[str], T], s: str, n: int, _min: T = None, _max: T = None) -> list[T] | None:
    """Парсит строку чисел."""
    tokens = s.strip().split(' ')

    row = []

    for token in tokens:
        number = _parse_number(
            basic_parser,
            token,
            _min,
            _max,
        )

        if not number:
            return None

        row.append(number)

    if len(row) != n:
        return None

    return row


# Парсит строку целых чисел, разделенных пробелами.
def parse_int_row(s: str, n: int, _min: int = None, _max: int = None) -> list[int] | None:
    """Парсит строку int-ов."""
    return _parse_number_row(int, s, n, _min, _max)


# Парсит строку чисел с плавающей точкой, разделенных пробелами.
def parse_float_row(s: str, n: int, _min: float = None, _max: float = None) -> list[float] | None:
    """Парсит строку float-ов."""
    return _parse_number_row(_float, s, n, _min, _max)
