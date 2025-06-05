# Модуль определяет обёртку для функций и список доступных функций для интегрирования

from dataclasses import dataclass
from typing import Callable
from math import exp, log, log10

# Датакласс для представления математической функции и её свойств.
@dataclass
class Function:
    """
    Обёртка для математической функции:
      f       – callable: сама функция от x,
      name    – строковое представление функции,
      nuh_uhs – список интервалов разрыва (кортежи (a, b)), где функция не определена или имеет разрыв.
      start   – левая граница области определения (может быть None).
      end     – правая граница области определения (может быть None).
    """
    f: Callable[[float], float]
    name: str
    nuh_uhs: list[tuple[float, float]]
    start: float | None # Уточнен тип
    end: float | None   # Уточнен тип

    # Безопасное вычисление значения функции в точке x.
    # Если вычисление f(x) вызывает исключение, пытается вычислить f(x + e).
    # Если и это не удается, возвращает 0.
    # e: Малое смещение для попытки обхода точки разрыва.
    def safe_f(self, x: float, e: float) -> float:
        """Вычисляет f(x); при исключении пробует f(x+e), иначе возвращает 0."""
        try:
            return self.f(x)
        except Exception:
            try:
                return self.f(x + e)
            except Exception:
                return 0

    # Проверяет, сходится ли функция в точке x.
    # Функция считается сходящейся, если f(x) вычисляется без исключений
    # и результат не является комплексным числом.
    def is_convergent_in_x(self, x: float) -> bool:
        """
        Проверяет, сходится ли функция в точке x:
          – вычисляет f(x), ловит исключения,
          – проверяет, что результат не комплексный.
        """
        try:
            y = self.f(x)
        except Exception:
            return False
        # Проверка, что результат не является комплексным числом.
        if isinstance(y, complex):
            return False
        return True

    # Проверяет, находится ли точка x вне интервалов разрыва (nuh_uhs).
    # Также проверяет, находится ли x в пределах границ области определения (start, end), если они заданы.
    def is_x_ok(self, x: float) -> bool:
        """
        Проверяет, не попадает ли x в запрещённые интервалы nuh_uhs
        и находится ли в границах [start, end].
        Возвращает False, если x ∈ [a, b] для любого (a, b) в nuh_uhs,
        или если x < start или x > end (если start/end заданы).
        """
        # Проверка на попадание в интервалы разрыва.
        for a, b in self.nuh_uhs:
            if a <= x <= b:
                return False
        # Проверка левой границы области определения.
        if self.start is not None and x < self.start:
            return False
        # Проверка правой границы области определения.
        if self.end is not None and x > self.end:
            return False
        return True

# Список функций, доступных для выбора пользователем в приложении.
FUNCTIONS = [
    # Квадратичная функция x^2 + 3x - 4. Определена везде.
    Function(lambda x: x ** 2 + 3 * x - 4, 'x^2 + 3x - 4', [], None, None),
    # Линейная функция 3x. Определена везде.
    Function(lambda x: 3 * x, '3x', [], None, None),
    # Экспоненциальная функция e^(x/2). Определена везде.
    Function(lambda x: exp(x / 2), 'e^{x / 2}', [], None, None),
    # Функция обратной пропорциональности 1/x. Имеет разрыв в точке x=0.
    Function(lambda x: 1 / x, '1 / x', [(0, 0)], None, None), # Интервал разрыва [0, 0] означает точку 0.
    # Логарифмическая функция log_x(3). Определена для x > 0 и x != 1.
    # nuh_uhs включает (-inf, 0] и точку x=1. start=0 ограничивает слева.
    Function(lambda x: log(3, x), 'log_x(3)', [(-1e1000, 0), (1, 1)], None, None),

    Function(lambda x: log(x, 3), 'log_3(x)', [(-1e1000, 0), (1, 1)], 0, None),

]
