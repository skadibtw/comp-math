import matplotlib.pyplot as plt  # type: ignore
import pandas as pd
from functions import FUNCTIONS

from methods import METHODS
from input import read_choice_from_stdin, read_float_from_stdin


def draw_plot(short_results: list[dict]):
    for short_result in short_results:
        xs, ys = short_result['xs'], short_result['ys']
        plt.plot(xs, ys, label=short_result['name'])

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()


def main():
    function_index = read_choice_from_stdin(
        'Выберите метод',
        [function['name'] for function in FUNCTIONS],
    )
    function = FUNCTIONS[function_index]
    f = function['f']
    compute_constant = function['compute_constant']
    integral = function['integral']

    x0 = read_float_from_stdin('Введите x0')
    y0 = read_float_from_stdin('Введите y0')
    xn = read_float_from_stdin('Введите xn')
    h = read_float_from_stdin('Введите h')
    e = read_float_from_stdin('Введите точность')

    const = compute_constant(x0, y0) # Константа для точного решения и методов

    short_results = []

    for method in METHODS:
        name = method['name']
        action = method['action']
        print(name)
        h_ = h

        xs, ys = [], []

        if method['one_step']:
            get_precision = method['get_precision']
            epsilon = get_precision(f, y0, x0, xn, h_, h_ / 2)
            while epsilon > e:
                h_ = h_ / 2
                epsilon = get_precision(f, y0, x0, xn, h_, h_ / 2)
            print(f'Точность {name} по правилу Рунге: {epsilon:.8f}')
            xs, ys = action(f, x0, y0, xn, h_)
        else:
            # const = compute_constant(x0, y0) # Удалено - const вычисляется один раз выше
            print(f'{const=}') # Будет использована const, вычисленная выше
            diff = 1e10
            
            # Начальное значение h_ для многошаговых методов, если оно не было установлено
            if 'h_' not in locals() or h_ == 0: # h_ может быть не определено, если все предыдущие методы были одношаговыми
                h_ = h # Используем начальное h или другое подходящее значение
            if h_ <= 0: # Убедимся, что h_ положительно для деления
                h_ = abs(xn-x0)/100 if xn != x0 else 0.01


            while diff > e:
                _diff = -1e10
                # Убедимся, что h_ не становится слишком маленьким или нулевым
                if h_ < 1e-9 : # Предотвращение слишком малого шага
                    print(f"Шаг h_ стал слишком маленьким ({h_}), прерывание для метода {name}")
                    break
                h_ /= 2
                if h_ < 1e-9 : # Повторная проверка после деления
                    print(f"Шаг h_ стал слишком маленьким ({h_}) после деления, прерывание для метода {name}")
                    break

                xs, ys = action(f, x0, y0, xn, h_)
                if not xs: # Если action вернул пустые списки (например, из-за проблем с шагом)
                    print(f"Метод {name} не смог вычислить точки с шагом {h_}.")
                    break 
                
                # n = int((xn - x0) / h) # Ошибка: здесь должно быть h_
                # Исправлено:
                if h_ == 0: # Предотвращение деления на ноль
                    print(f"Шаг h_ равен нулю для метода {name}, невозможно вычислить n.")
                    break
                n = int(round((xn - x0) / h_)) # Используем round для большей точности при определении n

                for i in range(len(xs)): # Используем len(xs) вместо n + 1 для безопасности
                    if i < len(ys): # Убедимся, что индекс не выходит за пределы ys
                         _diff = max(abs(ys[i] - integral(xs[i], const)), _diff)
                diff = _diff
            
            if diff > e and h_ < 1e-8 : # Если точность не достигнута, но шаг уже очень мал
                 print(f"Не удалось достичь требуемой точности {e:.8f} для метода {name}. Текущая точность: {diff:.8f} с шагом {h_:.8f}")
            else:
                print(f'Точность {name}: {diff:.8f}')
        
        print(' x | y ')
        for x, y in zip(xs, ys):
            print(f'{x} | {y}')

        short_results.append(dict(
            name=name,
            xs=xs,
            ys=ys,
        ))

        print()

    # Добавление точного решения для графика
    num_plot_points = 501  # Количество точек для гладкой кривой
    xs_exact = []
    ys_exact = []

    if abs(xn - x0) < 1e-9:  # Если x0 примерно равно xn
        xs_exact = [x0]
        ys_exact = [integral(x0, const)]
    else:
        step_exact = (xn - x0) / (num_plot_points - 1)
        xs_exact = [x0 + i * step_exact for i in range(num_plot_points)]
        # Гарантируем, что последняя точка точно xn
        if xs_exact:
            xs_exact[-1] = xn
        ys_exact = [integral(x, const) for x in xs_exact]

    short_results.append(dict(
        name='Точное решение',
        xs=xs_exact,
        ys=ys_exact,
    ))

    draw_plot(short_results)


if __name__ == '__main__':
    main()
