import matplotlib.pyplot as plt  # type: ignore
import pandas as pd

from actions import ACTIONS
from finite_diff import get_finite_diffs
from methods import METHODS
from dots import Dots
from input import read_choice_from_stdin, read_float_from_stdin
from methods.newton_div import get_newton_polynomial, newton_div, get_factors
from methods.newton_equidistant import newton_equidistant, _format_backward_polynomial, _format_forward_polynomial
from methods.lagrange import lagrange, lagrange_print
def draw_plot(dots: Dots, short_results: list[dict]):
    # строим графики в отдельных окнах для каждого метода
    xs_all = dots.get_xs()
    min_x, max_x = min(xs_all), max(xs_all)
    # сетка для кривой
    PLOT_XS = [min_x + (max_x - min_x) * i / 100 for i in range(101)]
    for short_result in short_results:
        if short_result['func'] is None:
            continue
        plt.figure()  # новое окно
        # рисуем узлы
        for x, y in dots.get_paired():
            plt.plot(x, y, 'ko')
        # рисуем точку интерполяции
        plt.plot(short_result['x'], short_result['y'], 'o', label=short_result['name'])
        # рисуем кривую
        ys = [short_result['func'](dots, x) for x in PLOT_XS]
        plt.plot(PLOT_XS, ys, label=short_result['base_name'])
        # границы по y с запасом
        all_ys = [y for _, y in dots.get_paired()] + ys
        min_y, max_y = min(all_ys), max(all_ys)
        diff_y = max_y - min_y or 1
        pad = diff_y * 0.2
        plt.ylim(min_y - pad, max_y + pad)
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.show()


def main():
    action_index = read_choice_from_stdin(
        'Выберите действие',
        [action['name'] for action in ACTIONS],
    )
    action = ACTIONS[action_index]['func']

    dots = action()
    print()

    finite_diffs = get_finite_diffs(dots)
    
    # добавляем имена колонок: 'x', 'y', 'Δ1y', 'Δ2y', …
    cols = ['x', 'y'] + [f'Δ{order}y' for order in range(1, len(finite_diffs))]
    print('Таблица конечных разностей:')
    print(pd.DataFrame(finite_diffs, columns=cols))

    # таблица разделённых разностей
    print('Таблица разделённых разностей:')
    divided_diffs = get_factors(dots)
    # формируем колонки для разделённых разностей
    div_cols = ['x'] + [f'd{order}' for order in range(1, len(divided_diffs))]
    # создаем DataFrame: берем первую строку каждого столбца
    div_table = [[dots.get_xs()[i]] + [divided_diffs[i][j] for j in range(1, len(div_cols))] for i in range(len(divided_diffs))]
    print(pd.DataFrame(div_table, columns=div_cols))
    

    # определяем X: из файла или запрашиваем у пользователя
    if hasattr(dots, 'selected_x'):
        X = dots.selected_x
    else:
        X = read_float_from_stdin(
            'Введите точку поиска: ',
            lambda x: min(dots.get_xs()) <= x <= max(dots.get_xs()),
        )

    short_results = []

    for method in METHODS:
        name = method['name']
        print(name)
        try:
            Y = method['func'](dots, X)
        except ValueError as e:
            print(f'Невозможно применить {name}: {e}')
            print()
            continue

        print(f'Y = {Y}')
        # для метода Ньютона один раз выводим формулу
        if method['func'] is newton_div:
            print(f'Полином Ньютона с разделенными разностями: {get_newton_polynomial(dots)}')
        print()
        if method['func'] is newton_equidistant:
            if X > dots.get_xs()[dots.get_n() // 2]:
                print('Интерполирование вперед ')
                print(f" {_format_backward_polynomial(dots)}")
            else: 
                print('Интерполирование назад')
                print(f"{_format_forward_polynomial(dots)}")
        if method['func'] is lagrange:
            print(*lagrange_print)


        short_results.append(dict(
            base_name=name,
            name=f'{name} (точка в ({X}; {Y}))',
            x=X,
            y=Y,
            func=method['func'] if method['draw'] else None,
        ))

    draw_plot(dots, short_results)


if __name__ == '__main__':
    main()
