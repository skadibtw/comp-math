# Лабораторная работа #4

import numpy as np
# Импортируем необходимые модули
from approximations import ALL_FUNCTIONS # Импортируем список функций
from plotting import plot
from io_handler import getdata_file, getdata_input, DEFAULT_FILE_IN

def print_results_table(answers):
    """ Вывод таблицы с результатами аппроксимации """
    print("\n\nРезультаты аппроксимации:")
    print("-" * 85) # Увеличим ширину для нового столбца
    print("%25s%15s%15s%15s%15s" % ("Вид функции", "S", "σ", "R^2", "Пирсон (лин.)"))
    print("-" * 85)
    for answer in answers:
        # Проверка наличия и корректности значений перед форматированием
        s_str = f"{answer['s']:.4f}" if answer.get('s') is not None and not np.isnan(answer['s']) else "----"
        stdev_str = f"{answer['stdev']:.4f}" if answer.get('stdev') is not None and not np.isnan(answer['stdev']) else "----"
        r_squared_str = f"{answer['r_squared']:.4f}" if answer.get('r_squared') is not None and not np.isnan(answer['r_squared']) else "----"
        pearson_str = f"{answer['pearson_r']:.4f}" if answer.get('pearson_r') is not None and not np.isnan(answer['pearson_r']) else "----"

        # Для нелинейных функций коэффициент Пирсона не выводится
        if answer['str_f'] != "fi = a*x + b":
            pearson_str = "----"

        print("%25s%15s%15s%15s%15s" % (answer['str_f'], s_str, stdev_str, r_squared_str, pearson_str))
    print("-" * 85)

def print_best_fit_details(best_answer, x_orig, y_orig):
    """ Вывод деталей наилучшей аппроксимации и таблицы значений """
    print("\nНаилучшая аппроксимирующая функция (по мин. среднеквадратичному отклонению):")
    print(f" {best_answer['str_f']}, где:")

    # Округляем коэффициенты до 4 знаков после запятой
    coeffs = {k: v for k, v in best_answer.items() if k in ['a', 'b', 'c', 'd']}
    for name, value in sorted(coeffs.items()): # Сортируем для порядка a, b, c, d
        print(f"  {name} = {round(value, 4)}")

    print(f"\nМера отклонения (S): {best_answer['s']:.4f}")
    print(f"Среднеквадратичное отклонение: {best_answer['stdev']:.4f}")

    # Вывод R^2 и интерпретации
    best_r2 = best_answer.get('r_squared')
    if best_r2 is not None and not np.isnan(best_r2):
        print(f"Коэффициент детерминации (R^2): {best_r2:.4f}")
        if best_r2 >= 0.95: interpretation = "высокая точность аппроксимации."
        elif best_r2 >= 0.8: interpretation = "хорошая точность аппроксимации."
        elif best_r2 >= 0.6: interpretation = "удовлетворительная аппроксимация."
        elif best_r2 >= 0.4: interpretation = "слабая аппроксимация."
        else: interpretation = "очень слабая или отсутствующая аппроксимация."
        print(f"  Интерпретация: {interpretation}")
    else:
        print("Коэффициент детерминации (R^2): Не удалось вычислить.")

    # Вывод таблицы значений
    print("\nТаблица значений для наилучшей аппроксимации:")
    print("-" * 60)
    print("%15s%15s%15s%15s" % ("x_i", "y_i", "phi(x_i)", "e_i"))
    print("-" * 60)
    best_f = best_answer['f']
    for i in range(len(x_orig)):
        xi = x_orig[i]
        yi = y_orig[i]
        try:
            phi_xi = best_f(xi)
            # Проверяем, не является ли результат NaN или Inf
            if np.isnan(phi_xi) or np.isinf(phi_xi):
                 print("%15.4f%15.4f%15s%15s" % (xi, yi, "Invalid", "Invalid"))
                 continue
            ei = yi - phi_xi
            print("%15.4f%15.4f%15.4f%15.4f" % (xi, yi, phi_xi, ei))
        except (ValueError, TypeError, OverflowError): # Ловим возможные ошибки при вычислении
             print("%15.4f%15.4f%15s%15s" % (xi, yi, "Error", "Error"))
    print("-" * 60)


if __name__ == "__main__":
    print("\tЛабораторная работа #4 (13)")
    print("АППРОКСИМАЦИЯ ФУНКЦИИ МЕТОДОМ НАИМЕНЬШИХ КВАДРАТОВ")

    data = None
    while data is None: # Цикл до успешного получения данных
        print(f"\nВзять исходные данные из файла ('{DEFAULT_FILE_IN}') (+) или ввести с клавиатуры (-)?")
        inchoice = input("Режим ввода (+/-): ").strip()
        if inchoice == '+':
            data = getdata_file() # Используем путь по умолчанию
            if data is None:
                print("\nНе удалось прочитать данные из файла. Попробуйте ввести вручную.")
        elif inchoice == '-':
            data = getdata_input()
        else:
            print("Некорректный выбор. Введите '+' или '-'.")

    # Выполнение аппроксимаций
    answers = []
    for func in ALL_FUNCTIONS:
        try:
            result = func(data['dots'])
            if result is not None:
                answers.append(result)
        except Exception as e:
            # Ловим ошибки на уровне вызова аппроксимирующей функции
            print(f"Ошибка при вычислении аппроксимации {func.__name__}: {e}")


    if not answers:
        print("\nНе удалось построить ни одной аппроксимирующей функции для данных точек.")
        input("\nНажмите Enter, чтобы выйти.")
        exit()

    # Сортировка результатов по возрастанию среднеквадратичного отклонения
    answers.sort(key=lambda z: z.get('stdev', float('inf'))) # float('inf') если stdev нет

    # Вывод таблицы результатов
    print_results_table(answers)

    # Подготовка данных для графика
    x_orig = np.array([dot[0] for dot in data['dots']])
    y_orig = np.array([dot[1] for dot in data['dots']])

    # Генерируем точки для графика только если есть данные
    if len(x_orig) > 0:
        try:
            x_min, x_max = np.min(x_orig), np.max(x_orig)
            # Добавляем небольшой отступ, если min и max равны
            if x_min == x_max:
                plot_x = np.array([x_min]) # Только одна точка
            else:
                plot_x = np.linspace(x_min, x_max, 200) # Больше точек для гладкости

            plot_y = []
            labels = []
            for answer in answers:
                plot_y_vals = []
                f = answer['f']
                for val in plot_x:
                    try:
                        y_val = f(val)
                        # Заменяем очень большие/маленькие числа и inf на NaN для корректной отрисовки
                        if not np.isfinite(y_val):
                            y_val = np.nan
                        plot_y_vals.append(y_val)
                    except (ValueError, TypeError, OverflowError):
                        plot_y_vals.append(np.nan) # Используем NaN для ошибок
                plot_y.append(plot_y_vals)
                labels.append(answer['str_f'])
            # Построение графика
            plot(x_orig, y_orig, plot_x, plot_y, labels)

        except Exception as e:
            print(f"\nОшибка при подготовке данных для графика или построении графика: {e}")
    else:
        print("\nНедостаточно данных для построения графика.")


    # Вывод деталей наилучшей аппроксимации
    best_answer = answers[0] # Так как отсортировали по stdev
    print_best_fit_details(best_answer, x_orig, y_orig)
    for answer in answers:
        print(answer['str_f'])
        if answer['a']:
            print('a = ', answer['a'])
        else:
            print('a = 0')
        if answer['b']:
            print('b = ', answer['b'])
        else:
            print('b = 0')    
        try:
            if answer['c']:
                print('c = ', answer['c'])
            else:
                print('c = 0')  
            
        except KeyError:
            pass
        try:
            if answer['d']:
                print('d = ', answer['c'])
            else:
                print('d = 0')  
        except KeyError:
            pass

    input("\n\nНажмите Enter, чтобы выйти.")

