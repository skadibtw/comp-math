from typing import Any, Callable
from common import EPS
from dots import Dots

from parse import parse_int, parse_float


def _is_float_or_int(n: Any) -> bool:
    """Проверяет, является ли n float или int."""
    return isinstance(n, int) or isinstance(n, float)


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


def read_choice_from_stdin(message: str, choices: list[Any]) -> int:
    """Выбор из списка. Возвращает выбранный индекс."""
    choice_count = len(choices)

    s = f'{message} [1-{choice_count}]:'

    for i, choice in enumerate(choices):
        s += f'\n{i + 1}. {choice}'

    index = read_int_from_stdin(s, lambda n: 1 <= n <= choice_count)
    index -= 1

    return index


def read_dots_from_stdin() -> list[tuple[float, float]]:
    dot_count = read_int_from_stdin('Кол-во точек:', lambda x: x > 0)

    xs = []
    ys = []

    for i in range(dot_count):
        print(f'Точка #{i + 1}')
        x = read_float_from_stdin('Введите X:')
        while x in xs:
            x += EPS
        y = read_float_from_stdin('Введите Y:')
        xs.append(x)
        ys.append(y)
    
    return Dots(xs, ys)


def read_dots_from_file() -> Dots:
    """
    Читает первую строку — X для интерполяции,
    затем каждая последующая строка: x y.
    """
    print('Введите путь к файлу с точками и X в первой строке:')
    path = input().strip()
    with open(path, 'r') as f:
        # первая строка — заданное X
        line = f.readline().strip()
        selected_x = parse_float(line)
        xs, ys = [], []
        for L in f:
            parts = L.strip().split()
            if len(parts) < 2:
                continue
            x = parse_float(parts[0])
            y = parse_float(parts[1])
            if x is None or y is None:
                continue
            xs.append(x)
            ys.append(y)
    dots = Dots(xs, ys)
    if selected_x is not None:
        setattr(dots, 'selected_x', selected_x)
    return dots
