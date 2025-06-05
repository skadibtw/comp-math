from math import log, exp, sqrt
import numpy as np
# Импортируем необходимые функции из utils
from utils import solve_det, calc_s, calc_stdev, calc_r_squared

def lin_func(dots):
    """ Линейная аппроксимация """
    data = {}
    n = len(dots)
    x = [dot[0] for dot in dots]
    y = [dot[1] for dot in dots]

    # Вычисление сумм, необходимых для метода наименьших квадратов
    sx = sum(x)
    sx2 = sum([xi ** 2 for xi in x])
    sy = sum(y)
    sxy = sum([x[i] * y[i] for i in range(n)])
    sy2 = sum([yi ** 2 for yi in y]) # Необходимо для коэффициента Пирсона

    # Решение системы линейных уравнений для нахождения коэффициентов a и b
    # | sx2 sx  | | a | = | sxy |
    # | sx  n   | | b |   | sy  |
    d = solve_det([[sx2, sx], [sx, n]]) # Определитель основной матрицы
    if abs(d) < 1e-10: return None # Если определитель близок к нулю, решения нет или оно не единственно
    d1 = solve_det([[sxy, sx], [sy, n]]) # Определитель для нахождения a
    d2 = solve_det([[sx2, sxy], [sx, sy]]) # Определитель для нахождения b
    a = d1 / d
    b = d2 / d
    data['a'] = a
    data['b'] = b

    # Определение аппроксимирующей функции
    f = lambda z: a * z + b
    data['f'] = f
    data['str_f'] = "fi = a*x + b" # Строковое представление функции
    # Расчет статистических показателей
    data['s'] = calc_s(dots, f) # Мера среднеквадратичного отклонения
    data['stdev'] = calc_stdev(dots, f) # Стандартное отклонение
    data['r_squared'] = calc_r_squared(dots, f) # Коэффициент детерминации

    # Расчет коэффициента корреляции Пирсона
    numerator = n * sxy - sx * sy
    denominator_sq = (n * sx2 - sx**2) * (n * sy2 - sy**2)
    if denominator_sq > 1e-10: # Проверка на деление на ноль
         data['pearson_r'] = numerator / sqrt(denominator_sq)
    else:
         data['pearson_r'] = float('nan') # Неопределенное значение, если знаменатель ноль

    return data

def sqrt_func(dots):
    """ Квадратичная аппроксимация """
    data = {}
    n = len(dots)
    x = [dot[0] for dot in dots]
    y = [dot[1] for dot in dots]

    # Вычисление сумм, необходимых для метода наименьших квадратов
    sx = sum(x)
    sx2 = sum([xi ** 2 for xi in x])
    sx3 = sum([xi ** 3 for xi in x])
    sx4 = sum([xi ** 4 for xi in x])
    sy = sum(y)
    sxy = sum([x[i] * y[i] for i in range(n)])
    sx2y = sum([(x[i] ** 2) * y[i] for i in range(n)])

    # Решение системы линейных уравнений для нахождения коэффициентов a, b, c
    # | n   sx  sx2 | | c | = | sy   |
    # | sx  sx2 sx3 | | b |   | sxy  |
    # | sx2 sx3 sx4 | | a |   | sx2y |
    d = solve_det([[n, sx, sx2], [sx, sx2, sx3], [sx2, sx3, sx4]]) # Определитель основной матрицы
    if abs(d) < 1e-10: return None # Если определитель близок к нулю, решения нет
    d1 = solve_det([[sy, sx, sx2], [sxy, sx2, sx3], [sx2y, sx3, sx4]]) # Определитель для c
    d2 = solve_det([[n, sy, sx2], [sx, sxy, sx3], [sx2, sx2y, sx4]]) # Определитель для b
    d3 = solve_det([[n, sx, sy], [sx, sx2, sxy], [sx2, sx3, sx2y]]) # Определитель для a

    c = d1 / d
    b = d2 / d
    a = d3 / d
    data['c'] = c
    data['b'] = b
    data['a'] = a

    # Определение аппроксимирующей функции
    f = lambda z: a * (z ** 2) + b * z + c
    data['f'] = f
    data['str_f'] = "fi = a*x^2 + b*x + c" # Строковое представление функции
    # Расчет статистических показателей
    data['s'] = calc_s(dots, f) # Мера среднеквадратичного отклонения
    data['stdev'] = calc_stdev(dots, f) # Стандартное отклонение
    data['r_squared'] = calc_r_squared(dots, f) # Коэффициент детерминации

    return data

def cube_func(dots):
    """ Кубическая аппроксимация """
    data = {}
    n = len(dots)
    x = [dot[0] for dot in dots]
    y = [dot[1] for dot in dots]

    # Вычисление сумм, необходимых для метода наименьших квадратов
    sx = sum(x); sx2 = sum(xi**2 for xi in x); sx3 = sum(xi**3 for xi in x)
    sx4 = sum(xi**4 for xi in x); sx5 = sum(xi**5 for xi in x); sx6 = sum(xi**6 for xi in x)
    sy = sum(y); sxy = sum(x[i]*y[i] for i in range(n))
    sx2y = sum(x[i]**2*y[i] for i in range(n)); sx3y = sum(x[i]**3*y[i] for i in range(n))

    # Матрица коэффициентов системы линейных уравнений
    main_matrix = [[n, sx, sx2, sx3], [sx, sx2, sx3, sx4], [sx2, sx3, sx4, sx5], [sx3, sx4, sx5, sx6]]
    # Вектор свободных членов
    free_coeffs = [sy, sxy, sx2y, sx3y]

    d = solve_det(main_matrix) # Определитель основной матрицы
    if abs(d) < 1e-10: return None # Если определитель близок к нулю, решения нет

    # Матрицы для нахождения коэффициентов по методу Крамера
    matrix_d = [[free_coeffs[0], sx, sx2, sx3], [free_coeffs[1], sx2, sx3, sx4], [free_coeffs[2], sx3, sx4, sx5], [free_coeffs[3], sx4, sx5, sx6]]
    matrix_c = [[n, free_coeffs[0], sx2, sx3], [sx, free_coeffs[1], sx3, sx4], [sx2, free_coeffs[2], sx4, sx5], [sx3, free_coeffs[3], sx5, sx6]]
    matrix_b = [[n, sx, free_coeffs[0], sx3], [sx, sx2, free_coeffs[1], sx4], [sx2, sx3, free_coeffs[2], sx5], [sx3, sx4, free_coeffs[3], sx6]]
    matrix_a = [[n, sx, sx2, free_coeffs[0]], [sx, sx2, sx3, free_coeffs[1]], [sx2, sx3, sx4, free_coeffs[2]], [sx3, sx4, sx5, free_coeffs[3]]]

    # Вычисление коэффициентов
    d_coeff = solve_det(matrix_d) / d; c_coeff = solve_det(matrix_c) / d
    b_coeff = solve_det(matrix_b) / d; a_coeff = solve_det(matrix_a) / d

    data['a'] = a_coeff; data['b'] = b_coeff; data['c'] = c_coeff; data['d'] = d_coeff

    # Определение аппроксимирующей функции
    f = lambda z: a_coeff * (z ** 3) + b_coeff * (z ** 2) + c_coeff * z + d_coeff
    data['f'] = f
    data['str_f'] = "fi = ax^3+bx^2+cx+d" # Строковое представление функции
    # Расчет статистических показателей
    data['s'] = calc_s(dots, f) # Мера среднеквадратичного отклонения
    data['stdev'] = calc_stdev(dots, f) # Стандартное отклонение
    data['r_squared'] = calc_r_squared(dots, f) # Коэффициент детерминации

    return data

def exp_func(dots):
    """ Экспоненциальная аппроксимация y = a * e^(b*x) """
    # Линеаризация: ln(y) = ln(a) + b*x. Пусть Y = ln(y), A = ln(a), B = b. Тогда Y = A + B*x
    data = {}
    n = len(dots)
    x = [dot[0] for dot in dots]
    y = []
    # Проверка, что все y > 0, так как логарифм от неположительного числа не определен
    for dot in dots:
        if dot[1] <= 0:
            print("Предупреждение: Экспоненциальная аппроксимация требует y > 0.")
            return None
        y.append(dot[1])

    # Линеаризация y
    lin_y = [log(yi) for yi in y]
    lin_dots = list(zip(x, lin_y)) # Новые точки для линейной аппроксимации
    
    # Применение линейной аппроксимации к линеаризованным данным
    lin_result = lin_func(lin_dots) 

    if lin_result is None: return None # Если линейная аппроксимация не удалась

    # Возвращение к исходным коэффициентам
    # lin_result['b'] это A = ln(a) => a = e^A
    # lin_result['a'] это B = b
    a = exp(lin_result['b']) 
    b = lin_result['a']
    data['a'] = a
    data['b'] = b

    # Определение аппроксимирующей функции
    f = lambda z: a * exp(b * z)
    data['f'] = f
    data['str_f'] = "fi = a*e^(b*x)" # Строковое представление функции
    # Расчет статистических показателей для исходных данных
    data['s'] = calc_s(dots, f)
    data['stdev'] = calc_stdev(dots, f)
    data['r_squared'] = calc_r_squared(dots, f)

    return data

def log_func(dots):
    """ Логарифмическая аппроксимация y = a*ln(x) + b """
    # Линеаризация: Пусть X = ln(x). Тогда y = a*X + b.
    data = {}
    n = len(dots)
    x = []
    y = [dot[1] for dot in dots]
    # Проверка, что все x > 0, так как логарифм от неположительного числа не определен
    for dot in dots:
        if dot[0] <= 0:
            print("Предупреждение: Логарифмическая аппроксимация требует x > 0.")
            return None
        x.append(dot[0])

    # Линеаризация x
    lin_x = [log(xi) for xi in x]
    lin_dots = list(zip(lin_x, y)) # Новые точки для линейной аппроксимации
    
    # Применение линейной аппроксимации к линеаризованным данным
    lin_result = lin_func(lin_dots)

    if lin_result is None: return None # Если линейная аппроксимация не удалась

    # Коэффициенты a и b напрямую получаются из линейной аппроксимации
    # lin_result['a'] это a
    # lin_result['b'] это b
    a = lin_result['a']
    b = lin_result['b']
    data['a'] = a
    data['b'] = b

    # Определение аппроксимирующей функции
    # Добавим проверку z > 0 в лямбда-функцию, чтобы избежать ошибки при вычислении log(z)
    f = lambda z: a * log(z) + b if z > 0 else float('nan')
    data['f'] = f
    data['str_f'] = "fi = a*ln(x) + b" # Строковое представление функции
    # Расчет статистических показателей для исходных данных
    data['s'] = calc_s(dots, f)
    data['stdev'] = calc_stdev(dots, f)
    data['r_squared'] = calc_r_squared(dots, f)

    return data

def pow_func(dots):
    """ Степенная аппроксимация y = a * x^b """
    # Линеаризация: ln(y) = ln(a) + b*ln(x). Пусть Y = ln(y), A = ln(a), B = b, X = ln(x). Тогда Y = A + B*X.
    data = {}
    n = len(dots)
    x = []
    y = []
    # Проверка, что все x > 0 и y > 0
    for dot in dots:
        if dot[0] <= 0:
            print("Предупреждение: Степенная аппроксимация требует x > 0.")
            return None
        if dot[1] <= 0:
            print("Предупреждение: Степенная аппроксимация требует y > 0.")
            return None
        x.append(dot[0])
        y.append(dot[1])

    # Линеаризация x и y
    lin_x = [log(xi) for xi in x]
    lin_y = [log(yi) for yi in y]
    lin_dots = list(zip(lin_x, lin_y)) # Новые точки для линейной аппроксимации
    
    # Применение линейной аппроксимации к линеаризованным данным
    lin_result = lin_func(lin_dots)

    if lin_result is None: return None # Если линейная аппроксимация не удалась

    # Возвращение к исходным коэффициентам
    # lin_result['b'] это A = ln(a) => a = e^A
    # lin_result['a'] это B = b
    a = exp(lin_result['b'])
    b = lin_result['a']
    data['a'] = a
    data['b'] = b

    # Определение аппроксимирующей функции
    # Добавим проверку z > 0 в лямбда-функцию, чтобы избежать ошибки при вычислении z**b для отрицательных z
    f = lambda z: a * (z ** b) if z > 0 else float('nan')
    data['f'] = f
    data['str_f'] = "fi = a*x^b" # Строковое представление функции
    # Расчет статистических показателей для исходных данных
    data['s'] = calc_s(dots, f)
    data['stdev'] = calc_stdev(dots, f)
    data['r_squared'] = calc_r_squared(dots, f)

    return data

# Список всех доступных функций аппроксимации
ALL_FUNCTIONS = [
    lin_func,
    sqrt_func,
    cube_func,
    exp_func,
    log_func,
    pow_func
]
