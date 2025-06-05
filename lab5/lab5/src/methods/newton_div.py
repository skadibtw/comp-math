"""Модуль реализует интерполяцию методом Ньютона через таблицу разделённых разностей."""

from common import rounded
from dots import Dots


def get_factors(dots: Dots):
    # Получаем число узлов интерполяции
    n = dots.get_n()

    # Инициализируем таблицу разделённых разностей размером n×n
    result = [
        ['' for _ in range(n)]
        for _ in range(n)
    ]

    xs = dots.get_xs()  # список x-координат
    ys = dots.get_ys()  # список y-координат

    # Первый столбец – нулевые порядки разностей (просто y)
    for i in range(n):
        result[i][0] = ys[i]
    #формула разделенных разностей 2 порядка f(x_i+1; x_i+2) - f(x_i, x_i+1) / x_i+2 - x_i
    # Вычисляем разделённые разности по рекуррентной формуле
    for i in range(1, n):
        for j in range(0, n - i):
            # Вычисляем знаменатель (разность x)
            denominator = xs[j + i] - xs[j]
            if denominator == 0:
                # Если попались дублирующиеся x, выбрасываем ошибку
                raise ValueError(f"Деление на 0: xs[{j+i}] == xs[{j}]")
            # Формула разделённых разностей:
            # f[x_j,...,x_{j+i}] = ( f[x_{j+1},...,x_{j+i}] - f[x_j,...,x_{j+i-1}] ) / (x_{j+i} - x_j)
            result[j][i] = (result[j + 1][i - 1] - result[j][i - 1]) / denominator

    return result


def newton_div(dots: Dots, X: float) -> float:
    """
    Оценивает интерполяционный полином Ньютона в точке X.
    """
    # Проверка на количество точек
    n = dots.get_n()
    if n == 0:
        raise ValueError("Cannot interpolate with zero points.")
    if n == 1:
        # Если единственная точка, возвращаем её y сразу с округлением
        return rounded(dots.get_ys()[0])

    # Строим таблицу разделённых разностей
    factors = get_factors(dots)

    xs = dots.get_xs()
    # Начальное значение полинома – f[x_0]
    result = factors[0][0]

    # Добавляем каждый следующий член вида f[x_0,...,x_i]·(X - x_0)...(X - x_{i-1})
    for i in range(1, n):
        q = factors[0][i]
        for j in range(0, i):
            q *= (X - xs[j])
        result += q

    # Округляем конечный результат
    return rounded(result)


def get_newton_polynomial(dots: Dots) -> str:
    """
    Строит строковое представление интерполяционного полинома Ньютона.
    """
    xs = dots.get_xs()
    factors = get_factors(dots)[0]
    n = dots.get_n()
    terms: list[str] = []
    for k in range(n):
        coeff = factors[k]
        # Пропускаем практически нулевые коэффициенты
        if abs(coeff) < 1e-12:
            continue
        # Форматируем коэффициент: без .0 если целый
        coeff_str = str(int(coeff)) if float(coeff).is_integer() else str(coeff)
        if k == 0:
            terms.append(f"{coeff_str}")
        else:
            mul = "*".join(f"(x - {xs[j]})" for j in range(k))
            terms.append(f"{coeff_str}*{mul}")
    return " + ".join(terms) if terms else "0"
