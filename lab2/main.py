import math

import matplotlib.pyplot as plt

import bisection
import iter
import newt
import sekushih

roundconst = 10  # точность вывода


def roundto(x: float):
    return x

def exitstr():
    print("Неверный ввод")


def tryto(x, func):
    try:
        return func(x)
    except Exception:
        return None


def inputf(st: str, func):
    x = tryto(input(st), func)
    while x is None:
        exitstr()
        x = tryto(input(st), func)
    return x


def get_function(choice):
    if choice == "1":
        # f(x) = 3x^3 + 1.7x^2 - 15.42x + 6.89
        f = lambda x: 3 * x ** 3 + 1.7 * x ** 2 - 15.42 * x + 6.89
        df = lambda x: 9 * x ** 2 + 3.4 * x - 15.42
        phi = lambda x: x - 0.018 * (3 * x ** 3 + 1.7 * x ** 2 - 15.42 * x + 6.89)
    elif choice == "2":
        # f(x) = -1.8x^3 - 2.94x^2 + 10.37x + 5.38
        f = lambda x: -1.8 * x ** 3 - 2.94 * x ** 2 + 10.37 * x + 5.38
        df = lambda x: -5.4 * x ** 2 - 5.88 * x + 10.37
        phi = lambda x: x + 0.0383 * (-1.8 * x ** 3 - 2.94 * x ** 2 + 10.37 * x + 5.38)
    elif choice == "3":
        # f(x) = x^3 - 3.125x^2 - 3.5x + 2.458
        f = lambda x: x ** 3 - 3.125 * x ** 2 - 3.5 * x + 2.458
        df = lambda x: 3 * x ** 2 - 6.25 * x - 3.5
        phi = lambda x: x - 0.0512 * (x ** 3 - 3.125 * x ** 2 - 3.5 * x + 2.458)
    elif choice == "4":
        # Трансцендентная функция: f(x) = cos(x) - x
        f = lambda x: math.cos(x) - x
        df = lambda x: -math.sin(x) - 1
        phi = lambda x: math.cos(x)
    else:
        print("Неверный выбор функции. Используется функция 1.")
        return get_function("1")
    return f, df, phi


def get_system(choice):
    if choice == "1":
        # Система 1:
        # 2x - sin(y - 0.5) = 1
        # y + cos(x) = 1.5
        def f1(x, y):
            return 2 * x - math.sin(y - 0.5) - 1

        def f2(x, y):
            return y + math.cos(x) - 1.5

        def phi1(x, y):
            return (math.sin(y - 0.5) + 1) / 2

        def phi2(x, y):
            return 1.5 - math.cos(x)

        def F(p):
            return [f1(p[0], p[1]), f2(p[0], p[1])]

        def J(p):
            return [[2, -math.cos(p[1] - 0.5)],
                    [-math.sin(p[0]), 1]]
    elif choice == "2":
        # Система 2:
        # sin(x+y) - 1.5x + 0.1 = 0
        # x^2 + 2y^2 - 1 = 0
        def f1(x, y):
            return math.sin(x + y) - 1.5 * x + 0.1

        def f2(x, y):
            return x ** 2 + 2 * y ** 2 - 1

        def phi1(x, y):
            return (math.sin(x + y) + 0.1) / 1.5

        def phi2(x, y):
            return math.sqrt(max(0, (1 - x ** 2) / 2))

        def F(p):
            return [f1(p[0], p[1]), f2(p[0], p[1])]

        def J(p):
            return [[math.cos(p[0] + p[1]) - 1.5, math.cos(p[0] + p[1])],
                    [2 * p[0], 4 * p[1]]]
    elif choice == "3":
        # Система 3:
        # cos(y - 2) + x = 0
        # sin(x + 0.5) - y - 1 = 0
        def f1(x, y):
            return math.cos(y - 2) + x

        def f2(x, y):
            return math.sin(x + 0.5) - y - 1

        def phi1(x, y):
            return -math.cos(y - 2)

        def phi2(x, y):
            return math.sin(x + 0.5) - 1

        def F(p):
            return [f1(p[0], p[1]), f2(p[0], p[1])]

        def J(p):
            return [[1, -math.sin(p[1] - 2)],
                    [math.cos(p[0] + 0.5), -1]]
    else:
        print("Неверный выбор системы. Используется система 1.")
        return get_system("1")
    return f1, f2, phi1, phi2, F, J


def read_values():
    input_choice = input("Введи 0 если хочешь ввести с клавиатуры входные данные, и иное от 0 если хочешь из файла: ")
    if input_choice == "0":
        a = inputf('Введи левую границу = ', float)
        b = inputf('Введи правую границу = ', float)
        eps = inputf('Введи погрешность = ', float)
        return a, b, eps
    else:
        file_name = input("Введите имя файла: ")
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    a = float(lines[0].strip())
                    b = float(lines[1].strip())
                    eps = float(lines[2].strip())
                    return a, b, eps
                else:
                    print("Файл не содержит достаточно строк")
                    exit(1)
        except FileNotFoundError:
            print(f"Файл {file_name} не найден")
            exit(1)


def read_system_values():
    input_choice = input("Введи 0 если хочешь ввести с клавиатуры входные данные, и иное от 0 если хочешь из файла: ")
    if input_choice == "0":
        x0 = inputf('Введи начальное приближение x0 = ', float)
        y0 = inputf('Введи начальное приближение y0 = ', float)
        eps = inputf('Введи погрешность = ', float)
        return x0, y0, eps
    else:
        file_name = input("Введите имя файла: ")
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    x0 = float(lines[0].strip())
                    y0 = float(lines[1].strip())
                    eps = float(lines[2].strip())
                    return x0, y0, eps
                else:
                    print("Файл не содержит достаточно строк")
                    exit(1)
        except FileNotFoundError:
            print(f"Файл {file_name} не найден")
            exit(1)


def choice_method(f, df, phi, a, b, eps):
    print("На выбор 3 метода:")
    print("1. Метод половинного деления")
    print("2. Метод секущих")
    print("3. Метод простой итерации")
    type_choice = input("Выбери один из трех методов: ")
    try:
        if type_choice == "1":
            return bisection.bisection_method(f, a, b, eps)
        elif type_choice == "2":
            return sekushih.secant_method(f, a, b, eps)
        elif type_choice == "3":
            x0 = (a + b) / 2
            return iter.iter_method(f, phi, x0, eps, a, b)
        else:
            print("Неверный выбор метода. Попробуйте снова.")
            return choice_method(f, df, phi, a, b, eps)
    except ValueError as e:
        print(f"Ошибка: {str(e)}")
        print("Попробуйте другой метод или измените интервал.")
        return choice_method(f, df, phi, a, b, eps)


def output(x, y, i, fxy=None):
    output_choice = input("Введи 0 если хочешь вывести на экран, и иное от 0 если хочешь в файл: ")
    # обработка значения невязки: число или кортеж
    if fxy is None:
        s = ""
    elif isinstance(fxy, tuple):
        s = f", f1(x,y) = {fxy[0]}, f2(x,y) = {fxy[1]}"
    else:
        s = f", f(x) = {roundto(fxy)}"
    s1 = f"x = {roundto(x)}, {'y' if fxy is None or isinstance(fxy, tuple) else 'f(x)'} = {roundto(y)}, i = {i}{s}\n"
    if output_choice == "0":
        print(s1, end="")
    else:
        file_name = input("Введите имя файла: ")
        try:
            with open(file_name, 'w') as file:
                file.write(s1)
            print(f"Результаты сохранены в файл {file_name}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {str(e)}")


def plt_system(f, g):
    # Настройка окна графика (для matplotlib >= 3.4 можно использовать manager.set_window_title)
    plt.gcf().canvas.manager.set_window_title("График системы уравнений")
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, marker=">", ms=5, color='k',
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k',
            transform=ax.get_xaxis_transform(), clip_on=False)
    xRange = [i * 0.01 for i in range(-500, 501)]
    yRange = [i * 0.01 for i in range(-500, 501)]
    F = [[f(X, Y) for X in xRange] for Y in yRange]
    G = [[g(X, Y) for X in xRange] for Y in yRange]
    plt.contour(xRange, yRange, F, [0])
    plt.contour(xRange, yRange, G, [0])
    plt.grid(True)
    plt.title("Графики уравнений системы")
    plt.show()


def plt_function(f):
    plt.gcf().canvas.manager.set_window_title("График функции")
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, marker=">", ms=5, color='k',
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k',
            transform=ax.get_xaxis_transform(), clip_on=False)
    xRange = [i * 0.01 for i in range(-500, 501)]
    yRange = [f(X) for X in xRange]
    plt.plot(xRange, yRange)
    plt.grid(True)
    plt.title("График функции")
    plt.show()


def run():
    type_choice = input("Введи 0 если хочешь систему уравнений, и иное от 0 если хочешь уравнение: ")
    if type_choice == "0":
        print('На выбор дано 3 системы:')
        print('1. 2x - sin(y - 0.5) = 1')
        print('   y + cos(x) = 1.5\n')
        print('2. sin(x+y) = 1.5x - 0.1')
        print('   x^2 + 2y^2 = 1\n')
        print('3. cos(y - 2) + x = 0')
        print('   sin(x + 0.5) - y = 1\n')
        choice = input("Введи номер системы, которую надо решить: ")
        f1, f2, phi1, phi2, F, J = get_system(choice)
        plt_system(f1, f2)
        x0, y0, eps = read_system_values()
        initial_point = [x0, y0]
        result, iters = newt.newton_method_systems(F, J, initial_point, tol=eps)
        if result is None:
            print("Метод Ньютона не сошелся. Попробуйте другое начальное приближение.")
            return
        x, y = result[0], result[1]
        # Вывод результата через output с вычислением невязок для системы
        output(x, y, iters, (f1(x, y), f2(x, y)))
    else:
        print('На выбор дано 3 уравнения:')
        print('1. 3x^3 + 1.7x^2 - 15.42x + 6.89\n')
        print('2. -1.8x^3 - 2.94x^2 + 10.37x + 5.38\n')
        print('3. x^3 - 3.125x^2 - 3.5x + 2.458\n')
        print('4. cos(x) - x\n')
        choice = input("Введи номер функции, которую надо решить: ")
        f, df, phi = get_function(choice)
        plt_function(f)
        a, b, eps = read_values()
        try:
            x, y, i = choice_method(f, df, phi, a, b, eps)
            output(x, y, i)
        except Exception as e:
            print(f"Ошибка при решении уравнения: {str(e)}")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        exit(-1)
