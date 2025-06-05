import numpy as np
from math import sqrt

def solve_minor(matrix, i, j):
    """ Найти минор элемента матрицы """
    n = len(matrix)
    return [[matrix[row][col] for col in range(n) if col != j] for row in range(n) if row != i]


def solve_det(matrix):
    """ Найти определитель матрицы """
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sgn = 1
    for j in range(n):
        det += sgn * matrix[0][j] * solve_det(solve_minor(matrix, 0, j))
        sgn *= -1
    return det


def calc_s(dots, f):
    """ Найти меру отклонения """
    n = len(dots)
    x = [dot[0] for dot in dots]
    y = [dot[1] for dot in dots]
    s = 0
    for i in range(n):
        try:
            fi = f(x[i])
            if np.isnan(fi): # Пропускаем NaN значения при расчете S
                continue
            s += (fi - y[i]) ** 2
        except (ValueError, TypeError): # Пропускаем ошибки вычисления функции
            continue
    return s


def calc_stdev(dots, f):
    """ Найти среднеквадратичное отклонение """
    n = len(dots)
    if n == 0:
        return float('nan')
    
    # Пересчитаем количество точек, для которых f(x) не NaN
    valid_count = 0
    x = [dot[0] for dot in dots]
    for i in range(n):
        try:
            if not np.isnan(f(x[i])):
                valid_count += 1
        except (ValueError, TypeError):
            continue # Пропускаем точки, где функция не может быть вычислена

    if valid_count == 0:
        return float('nan')

    s = calc_s(dots, f)
    return sqrt(s / valid_count)


def calc_r_squared(dots, f):
    """ Вычислить коэффициент детерминации R^2 """
    y_orig = np.array([dot[1] for dot in dots])
    x_orig = np.array([dot[0] for dot in dots])
    if len(y_orig) < 2:
        return float('nan') # Невозможно вычислить для < 2 точек

    y_pred = []
    valid_indices_mask = []
    for xi in x_orig:
        try:
            pred = f(xi)
            is_valid = not np.isnan(pred)
            y_pred.append(pred if is_valid else np.nan)
            valid_indices_mask.append(is_valid)
        except (ValueError, TypeError):
            y_pred.append(np.nan)
            valid_indices_mask.append(False)

    y_pred = np.array(y_pred)
    valid_indices = np.where(valid_indices_mask)[0]

    if len(valid_indices) < 2: # Need at least 2 valid points
        return float('nan')

    y = y_orig[valid_indices]
    y_pred_valid = y_pred[valid_indices]

    if len(y) < 2:
        return float('nan')

    y_mean = np.mean(y)
    ss_tot = np.sum((y - y_mean)**2)
    ss_res = np.sum((y - y_pred_valid)**2)

    if ss_tot < 1e-10: # Если все y одинаковы, R^2 не определен или равен 1 (если ss_res тоже 0)
        return 1.0 if ss_res < 1e-10 else float('nan')

    r_squared = 1 - (ss_res / ss_tot)
    return r_squared
