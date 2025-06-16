import matplotlib.pyplot as plt  # type: ignore
import pandas as pd
from functions import FUNCTIONS

from methods import METHODS
from input import read_choice_from_stdin, read_float_from_stdin


def draw_plot(method_result: dict, exact_result: dict):
    plt.figure() # Создаем новое окно для каждого графика
    
    # График численного метода
    xs_method, ys_method = method_result['xs'], method_result['ys']
    plt.plot(xs_method, ys_method, label=method_result['name'])

    # График точного решения
    xs_exact, ys_exact = exact_result['xs'], exact_result['ys']
    plt.plot(xs_exact, ys_exact, label=exact_result['name'], linestyle='--')

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.title(f"Сравнение: {method_result['name']} и Точное решение")
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

    method_outputs = [] # Сохраняем результаты каждого метода

    for method in METHODS:
        name = method['name']
        action = method['action']
        print(name)
        h_ = h

        xs, ys = [], []

        if method['one_step']:
            get_precision = method['get_precision']
            if True: # <5 если хотим вернуть проверку
                print("Считаем правило Рунге на конце интервала.")
                epsilon = get_precision(f, y0, x0, xn, h_, h_ / 2)
                xs, ys = action(f, x0, y0, xn, h_)
                print(f"Последнее значение при h = {h_}, x = {xs[-1]}, y = {ys[-1]}")
                while epsilon > e:
                    h_ = h_ / 2
                    xs, ys = action(f, x0, y0, xn, h_)
                    print(f"Последнее значение при h = {h_}, x = {xs[-1]}, y = {ys[-1]}")
                    epsilon = get_precision(f, y0, x0, xn, h_, h_ / 2)
                h_ = h_ / 2
                print(f'Шаг {name} по правилу Рунге: {h_:.8f}')
            '''
            else: 
                print("h > 5, считаем правило Рунге на каждом шаге.")
                # Проверяем точность на каждом шаге
                max_epsilon = 0
                current_x = x0
                while current_x < xn:
                    next_x = min(current_x + h_, xn)  # Не выходим за пределы интервала
                    epsilon = get_precision(f, y0, x0, next_x, h_, h_ / 2)
                    max_epsilon = max(max_epsilon, epsilon)
                    current_x = next_x
                
                # Если максимальная погрешность превышает допустимую, уменьшаем шаг
                while max_epsilon > e:
                    h_ = h_ / 2
                    max_epsilon = 0
                    current_x = x0
                    while current_x < xn:
                        next_x = min(current_x + h_, xn)
                        epsilon = get_precision(f, y0, x0, next_x, h_, h_ / 2)
                        max_epsilon = max(max_epsilon, epsilon)
                        current_x = next_x
                
                print(f'Максимальная точность {name} по правилу Рунге на всех шагах: {max_epsilon:.8f}')
            '''
            xs, ys = action(f, x0, y0, xn, h_)
        else:
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
                
                if h_ == 0: # Предотвращение деления на ноль
                    print(f"Шаг h_ равен нулю для метода {name}, невозможно вычислить n.")
                    break
                n = int(round((xn - x0) / h_)) # Используем round для большей точности при определении n
                print("x | y | y_точн | разность")
                for i in range(len(xs)):
                    if i < len(ys): # Убедимся, что индекс не выходит за пределы ys
                         _diff = max(abs(ys[i] - integral(xs[i], const)), _diff)
                         print(f'{xs[i]:6f} {ys[i]:6f} {integral(xs[i], const):6f} {_diff:6f}')

                diff = _diff
            
            if diff > e and h_ < 1e-8 : # Если точность не достигнута, но шаг уже очень мал
                 print(f"Не удалось достичь требуемой точности {e:.8f} для метода {name}. Текущая точность: {diff:.8f} с шагом {h_:.8f}")
            else:
                print(f'Точность {name}: {diff:.8f}')
        '''
        print(' x | y ')
        for x, y in zip(xs, ys):
            print(f'{x} | {y}')
        '''

        method_outputs.append(dict(
            name=name,
            xs=xs,
            ys=ys,
        ))

        # Выводим последнее значение метода
        if xs and ys:
            print(f'Последнее значение {name}: x = {xs[-1]:.8f}, y = {ys[-1]:.8f}')
            '''
            # Выводим значения функции в узловых точках исходного интервала
            print(f'Значения функции в узловых точках для {name}:')
            print('    x         |       y      ')
            print('-' * 30)
            
            # Генерируем узловые точки с исходным шагом h
            current_x = x0
            point_count = 0
            max_display_points = 10
            
            while current_x <= xn + 1e-10 and point_count < max_display_points:
                # Находим ближайший x в массиве xs или интерполируем
                y_value = None
                
                # Ищем точное совпадение или ближайшую точку
                for i, x_val in enumerate(xs):
                    if abs(x_val - current_x) < h * 0.01:  # Точка найдена
                        y_value = ys[i]
                        break
                
                # Если точной точки нет, делаем интерполяцию
                if y_value is None:
                    for i in range(len(xs)-1):
                        if xs[i] <= current_x <= xs[i+1]:
                            t = (current_x - xs[i]) / (xs[i+1] - xs[i])
                            y_value = ys[i] + t * (ys[i+1] - ys[i])
                            break
                
                if y_value is not None:
                    print(f'{current_x:10.6f} | {y_value:10.6f}')
                
                current_x += h
                point_count += 1
            
            total_nodes = int((xn - x0) / h) + 1
            if point_count < total_nodes:
                print(f'... и еще {total_nodes - point_count} точек')
            '''
        print()

    # Подготовка данных точного решения
    num_plot_points = 501
    xs_exact = []
    ys_exact = []

    if abs(xn - x0) < 1e-9:
        xs_exact = [x0]
        ys_exact = [integral(x0, const)]
    else:
        step_exact = (xn - x0) / (num_plot_points - 1)
        xs_exact = [x0 + i * step_exact for i in range(num_plot_points)]
        if xs_exact:
            xs_exact[-1] = xn
        ys_exact = [integral(x, const) for x in xs_exact]

    exact_solution_data = dict(
        name='Точное решение',
        xs=xs_exact,
        ys=ys_exact,
    )

    # Выводим последнее значение точного решения
    if xs_exact and ys_exact:
        print(f'Последнее значение точного решения: x = {xs_exact[-1]:.8f}, y = {ys_exact[-1]:.8f}')
        print()

    # Отображение графиков для каждого метода в отдельном окне
    for method_result in method_outputs:
        draw_plot(method_result, exact_solution_data)


if __name__ == '__main__':
    main()
