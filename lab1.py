import sys

import numpy as np


def solve_gauss_with_main_element(A, b):
    n = len(b)
    # Приводим A и b к типу float
    A = [list(map(float, row)) for row in A]
    b = list(map(float, b))

    sign = 1  # знак определителя

    # Прямой ход
    for k in range(n):
        # Поиск главного элемента в столбце k
        mainelem = k
        max_val = abs(A[k][k])
        for i in range(k + 1, n):
            if abs(A[i][k]) > max_val:
                max_val = abs(A[i][k])
                mainelem = i
        if abs(A[mainelem][k]) < 1e-12:
            raise ValueError("Матрица вырождена или почти вырождена.")
        # Если найденный главный элемент не на диагонали, меняем строки
        if mainelem != k:
            A[k], A[mainelem] = A[mainelem], A[k]
            b[k], b[mainelem] = b[mainelem], b[k]
            sign *= -1
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
            b[i] -= factor * b[k]

    # Вычисление определителя
    det = sign
    for i in range(n):
        det *= A[i][i]

    # Обратный ход: обратная подстановка для нахождения решения
    x = [0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = 0
        for j in range(i + 1, n):
            sum_ax += A[i][j] * x[j]
        x[i] = (b[i] - sum_ax) / A[i][i]

        return A, b, x, det


def compute_residuals(A_orig, b_orig, x):
    n = len(b_orig)
    r = [0] * n
    for i in range(n):
        sum_ax = 0
        for j in range(n):
            sum_ax += A_orig[i][j] * x[j]
        r[i] = sum_ax - b_orig[i]
    return r

def print_triangular_matrix(T, bT):
    """
    Выводит верхнетреугольную матрицу, где каждой строке соответствует преобразованный столбец bT.
    """
    n = len(bT)
    print("\nВерхнетреугольная матрица (с преобразованным столбцом b):")
    for i in range(n):
        # Формируем строку: коэффициенты и в конце свободный член
        row_str = " ".join(f"{T[i][j]:10.4f}" for j in range(len(T[i])))
        print(row_str, " |", f"{bT[i]:10.4f}")


def read_matrix_from_keyboard():
    n = int(input("Введите количество уравнений (n <= 20): "))
    if n > 20:
        print("Ошибка: размерность системы должна быть не более 20.")
        sys.exit(1)
    A = []
    b = []
    print("Введите каждое уравнение: коэффициенты и свободный член через пробел.")
    for i in range(n):
        row = list(map(float, input(f"Уравнение {i + 1}: ").split()))
        if len(row) != n + 1:
            print(f"Ошибка: в уравнении {i + 1} должно быть {n + 1} чисел.")
            sys.exit(1)
        A.append(row[:-1])
        b.append(row[-1])
    return A, b


def read_matrix_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        print("Ошибка: файл пустой или имеет неверный формат.")
        sys.exit(1)
    n = int(lines[0])
    if n > 20:
        print("Ошибка: размерность системы должна быть не более 20.")
        sys.exit(1)
    if len(lines) != n + 1:
        print(f"Ошибка: в файле должно быть {n + 1} строк, а найдено {len(lines)}.")
        sys.exit(1)
    A = []
    b = []
    for i in range(1, n + 1):
        parts = lines[i].split()
        if len(parts) != n + 1:
            print(f"Ошибка: в строке {i + 1} должно быть {n + 1} чисел.")
            sys.exit(1)
        row = list(map(float, parts))
        A.append(row[:-1])
        b.append(row[-1])
    return A, b


if __name__ == '__main__':
    print("Решение СЛАУ методом Гаусса")
    check = input("1: ввести матрицу с клавиатуры. 2: ввести матрицу из файла\n")
    solution = "Матрица не была введена корректно"
    A_orig = []
    b_orig = []
    if check == "1":
        A, b = read_matrix_from_keyboard()
        A_orig = A.copy()
        b_orig = b.copy()
        solution = solve_gauss_with_main_element(A, b)
    elif check == "2":
        filepath = input("Введите файл, в котором находится матрица: ")
        A, b = read_matrix_from_file(filepath)
        A_orig = A.copy()
        b_orig = b.copy()
        solution = solve_gauss_with_main_element(A, b)
    else:
        print("Команда не найдена")
        sys.exit(1)

    # Решение с использованием NumPy
    A_np = np.array(A_orig, dtype=float)
    b_np = np.array(b_orig, dtype=float)
    try:
        x_np = np.linalg.solve(A_np, b_np)
        det_np = np.linalg.det(A_np)
    except Exception as e:
        print("Ошибка при решении системы с помощью NumPy:", e)
        sys.exit(1)

    print("\nРезультаты, полученные с использованием библиотеки NumPy:")
    print("Вектор неизвестных:")
    for i, xi in enumerate(x_np):
        print(f"x[{i + 1}] = {xi:10.4f}")
    print("\nОпределитель системы (NumPy):", f"{det_np:10.4f}")
    print("Решение системы:", solution)

'''
def main():
    print("Выберите способ ввода системы уравнений:")
    print("1 - Ввод с клавиатуры")
    print("2 - Ввод из файла")
    choice = input("Ваш выбор (1 или 2): ").strip()

    if choice == "1":
        A, b = read_augmented_matrix_from_keyboard()
    elif choice == "2":
        filename = input("Введите имя файла: ").strip()
        try:
            A, b = read_augmented_matrix_from_file(filename)
        except Exception as e:
            print("Ошибка при чтении файла:", e)
            sys.exit(1)
    else:
        print("Неверный выбор. Завершение работы.")
        sys.exit(1)

    # Сохраняем исходную систему для вычисления невязок и сравнения с NumPy
    A_orig = copy.deepcopy(A)
    b_orig = b[:]

    try:
        T, bT, x, det = gaussian_elimination(A, b)
    except Exception as e:
        print("Ошибка при решении системы:", e)
        sys.exit(1)

    print_triangular_matrix(T, bT)

    print("\nВектор неизвестных (решение системы методом Гаусса):")
    for i, xi in enumerate(x):
        print(f"x[{i + 1}] = {xi:10.4f}")

    r = compute_residuals(A_orig, b_orig, x)
    print("\nВектор невязок (Ax - b) для найденного решения:")
    for i, ri in enumerate(r):
        print(f"r[{i + 1}] = {ri:10.4e}")

    print(f"\nВычисленный определитель методом Гаусса: {det:10.4f}")

    # Решение с использованием NumPy
    A_np = np.array(A_orig, dtype=float)
    b_np = np.array(b_orig, dtype=float)
    try:
        x_np = np.linalg.solve(A_np, b_np)
        det_np = np.linalg.det(A_np)
    except Exception as e:
        print("Ошибка при решении системы с помощью NumPy:", e)
        sys.exit(1)

    print("\nРезультаты, полученные с использованием библиотеки NumPy:")
    print("Вектор неизвестных:")
    for i, xi in enumerate(x_np):
        print(f"x[{i + 1}] = {xi:10.4f}")
    print("\nОпределитель системы (NumPy):", f"{det_np:10.4f}")

    # Сравнение результатов
    print("\nСравнение результатов:")
    print("Метод Гаусса и NumPy дают очень близкие (или совпадающие) результаты.")
    print(
        "Небольшие различия могут возникать из-за особенностей округления и внутренней реализации операций с плавающей точкой.")


if __name__ == '__main__':
    main()
'''