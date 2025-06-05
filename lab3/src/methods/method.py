from abc import abstractmethod
from functions import Function
from input import read_float_from_stdin
from typing import Tuple # Added import

# Начальное значение числа разбиения интервала интегрирования
N = 4


class Method:
    NAME: str
    e: float
    a: float
    b: float

    @property
    @abstractmethod
    def ACCURACY_ORDER(self) -> int:
        """Порядок точности метода (p для правила Рунге)."""
        raise NotImplementedError

    def read_input(self):
        self.e = read_float_from_stdin(f'Пожалуйста, введите валидную точность (>0)', lambda e: e > 0)
        self.a = read_float_from_stdin(f'Пожалуйста, введите валидный a')
        self.b = read_float_from_stdin(f'Пожалуйста, введите валидный b (>a)', lambda b: b > self.a)

    def _get_x(self, index, h) -> float:
        return self.a + index * h

    def _perform(self, func: Function, interval_count: int) -> float:
        raise NotImplementedError

    def _is_function_convergent_in_a(self, func: Function):
        return func.is_convergent_in_x(self.a)

    def _is_function_convergent_in_b(self, func: Function):
        return func.is_convergent_in_x(self.b)

    def _is_function_convergent_in_mid(self, func: Function):
        delta = self.e
        x = self.a + delta
        mid = (self.a + self.b) / 2

        if not func.is_convergent_in_x(mid):
            return False

        while x < self.b:
            if not func.is_convergent_in_x(x):
                return False
            x += delta

        return True

    def perform(self, func: Function) -> Tuple[float, int]: # Updated return type
        for c, d in func.nuh_uhs:
            # если отрезок [a,b] и интервал (c,d) пересекаются
            if not (self.b < c or self.a > d):
                print(f"Интервал интегрирования пересекает разрыв функции на [{c}, {d}].")
                raise ValueError("Нельзя интегрировать через точку разрыва.")
        if not self._is_function_convergent_in_a(func):
            print('Функция не существует в a.')
            raise ValueError('Функция не существует в a.')
        if not self._is_function_convergent_in_b(func):
            print('Функция не существует в b.')
            raise ValueError('Функция не существует в a.')
            

            
        if not self._is_function_convergent_in_mid(func):
            # This check might be too strict or inefficient. Consider refining or removing if issues arise.
            print('Функция не существует на отрезке. Интеграл не может быть вычислен.')
            raise ValueError('Функция не существует в a.')


        p = self.ACCURACY_ORDER
        runge_denominator = (2**p - 1)
        interval_count = N

        prev_area = self._perform(func, interval_count)
        interval_count *= 2
        area = self._perform(func, interval_count)
        iterations = 0
        max_iterations = 1000 # Limit iterations to prevent infinite loops

        # Runge rule loop
        while abs(area - prev_area) / runge_denominator > self.e:
            print("Количество разбиений:", interval_count)
            print("Площадь:", area)
            prev_area = area
            interval_count *= 2
            area = self._perform(func, interval_count)
            iterations += 1
            if iterations >= max_iterations:
                print(f'Превышено максимальное количество итераций ({max_iterations}). Точность может быть не достигнута.')
                break
            # Handle potential division by zero if prev_area is zero and area is also zero
            # This check was previously different, adjusting for Runge rule:
            # if prev_area == 0 and area == 0:
            #     print("Интеграл равен 0.")
            #     break # Exit if both are zero, likely integral is zero

        # Final check for convergence issues if area is still problematic (e.g., NaN, inf)
        if area != area or area == float('inf') or area == float('-inf'):
             print("Не удалось вычислить интеграл из-за расходимости или численных проблем.")
             # Consider returning a specific value or raising an error
             return float('nan'), interval_count


        return area, interval_count, prev_area
