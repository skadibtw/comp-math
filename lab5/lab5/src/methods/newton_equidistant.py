from common import EPS, rounded
from dots import Dots
from finite_diff import get_finite_diffs
import math

# Файл реализует интерполяцию методом Ньютона для равноотстоящих узлов:
# - Формирование строкового представления полиномов (прямой/обратный)
# - Проверка равномерности сетки
# - Прямой и обратный обход для вычисления значения функции

def _format_forward_polynomial(dots: Dots) -> str:
    """Форматирует полином прямого обхода для вывода."""
    # Получаем таблицу конечных разностей: finite_diffs[i][j] = Δ^i y в точке j
    finite_diffs = get_finite_diffs(dots)
    # Общее число узлов
    n = dots.get_n()
    
    # Инициализируем строку полинома с y₀
    polynomial = f"N_n(t) = {finite_diffs[0][1]:.4f}"

    for i in range(1, n):
        # Если i-ая разность выходит за границы таблицы, выходим
        if i + 1 >= len(finite_diffs[0]):
            break

        coeff = finite_diffs[0][i+1]
        # Пропускаем нулевые или очень маленькие коэффициенты
        if abs(coeff) < 1e-10:
            continue
        
        # Строим множитель t(t-1)...(t-(i-1))
        t_product = "t"
        if i > 1:
            for j in range(1, i):
                t_product += f"(t-{j})"
        
        # i! для правильного коэффициента
        factorial_val = math.factorial(i)
        
        # Выбираем знак в зависимости от coeff
        sign = " + " if coeff >= 0 else " - "
        # Добавляем новый член вида coeff * t_product / i!
        polynomial += f"{sign}{abs(coeff):.4f}*{t_product}/{factorial_val}"
    
    return polynomial


def _format_backward_polynomial(dots: Dots) -> str:
    """Форматирует полином обратного обхода для вывода."""
    # Получаем таблицу конечных разностей: finite_diffs[i][j] = Δ^i y в точке j
    finite_diffs = get_finite_diffs(dots)
    # Общее число узлов
    n = dots.get_n()
    
    # Инициализируем строку полинома с y_{n-1}
    polynomial = f"N_n(t) = {finite_diffs[n-1][1]:.4f}"

    for i in range(1, n):
        diff_index_row = n - 1 - i
        # столбец с Δⁱy сдвинут на +1
        diff_index_col = i + 1

        if diff_index_row < 0 or diff_index_col >= len(finite_diffs[0]):
            break
            
        coeff = finite_diffs[diff_index_row][diff_index_col]
        # Пропускаем нулевые или очень маленькие коэффициенты
        if abs(coeff) < 1e-10:
            continue
        
        # Формируем произведение t(t+1)(t+2)...(t+(i-1))
        t_product = "t"
        if i > 1:
            for j in range(1, i):
                t_product += f"(t+{j})"
        
        # Добавляем факториал в знаменатель
        factorial_val = math.factorial(i)
        
        # Выбираем знак в зависимости от coeff
        sign = " + " if coeff >= 0 else " - "
        # Добавляем новый член вида coeff * t_product / i!
        polynomial += f"{sign}{abs(coeff):.4f}*{t_product}/{factorial_val}"
    
    return polynomial


def _check_equidistancy(dots: Dots) -> bool:
    # Получаем число узлов и список абсцисс
    n = dots.get_n()
    xs = dots.get_xs()

    # Если менее двух точек — равномерность по условию
    if len(xs) < 2:
        return True

    # Шаг h между первыми двумя узлами
    h = rounded(xs[1] - xs[0])

    for i in range(1, n):
       # Сравниваем каждый следующий шаг с h с учётом EPS
       if rounded(xs[i] - xs[i - 1]) - h > EPS:
           return False

    return True
        

def newton_equidistant(dots: Dots, X: float) -> float:
    n = dots.get_n()
    xs = dots.get_xs()
    ys = dots.get_ys() # Необходимо для случая n=1

    if not _check_equidistancy(dots):
        raise ValueError('Точки не равноудалены')

    if n == 0:
        # Возвращаем 0.0 или можно выбросить исключение, если точек нет
        return 0.0 
    if n == 1:
        return rounded(ys[0])
    
    # Теперь n >= 2
    if X > xs[n // 2]:
        return newton_equidistant_backward(dots, X)


    h = xs[1] - xs[0]
    t = (X - xs[0]) / h

    finite_diff = get_finite_diffs(dots)

    # начинаем с y₀
    result = finite_diff[0][1]
    # фактор для построения t(t−1).../i!
    factor = 1

    for i in range(1, n):
        # на i-м шаге factor = t·(t−1)·...·(t−(i−1)) / i!
        factor *= (t - (i - 1)) / i
        # прибавляем i-ый член: Δ^i y₀ * factor
        result += finite_diff[0][i+1] * factor
    
    return rounded(result)


def newton_equidistant_backward(dots: Dots, X: float) -> float:
    n = dots.get_n()
    xs = dots.get_xs()
    ys = dots.get_ys()
    
    if not _check_equidistancy(dots):
        raise ValueError('Точки не равноудалены')

    if n == 0: # Добавлена проверка на n=0 для полноты
        return 0.0
    if n == 1: #
        return rounded(ys[0])
        # return 0.0

    # Теперь n >= 2
    h = xs[1] - xs[0] 
    t = (X - xs[n - 1]) / h

    finite_diffs = get_finite_diffs(dots)

    # стартуем с y_{n} в столбце 1
    result = finite_diffs[n-1][1] 
    
    factor = 1
    for i in range(1, n):
        factor *= (t + (i - 1)) / i
        
        diff_index_row = n - 1 - i
        diff_index_col = i + 1

        if diff_index_row < 0 or diff_index_col >= len(finite_diffs[0]): 
            break 
        
        # берем Δⁱy с нужной колонкой
        term_diff = finite_diffs[diff_index_row][diff_index_col]
        result += term_diff * factor
    
    return rounded(result)
