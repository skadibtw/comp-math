from functions import FUNCTIONS
from methods import METHODS
from input import read_choice_from_stdin


# Основная функция программы.
def main():
    # Запрос у пользователя выбора уравнения (функции).
    function_index = read_choice_from_stdin(
        'Выберите уравнение',
        [f.name for f in FUNCTIONS],
    )
    # Получение выбранного объекта функции.
    func = FUNCTIONS[function_index]

    # Запрос у пользователя выбора метода интегрирования.
    method_index = read_choice_from_stdin(
        'Выберите метод', # Исправлено сообщение
        [m.NAME for m in METHODS],
    )
    # Получение выбранного объекта метода.
    method = METHODS[method_index]

    # Чтение входных данных, специфичных для выбранного метода.
    method.read_input()

    # Выполнение расчета интеграла с использованием выбранного метода и функции.
    # Теперь perform возвращает кортеж (area, final_interval_count)
    area, final_interval_count, area2 = method.perform(func)

    # Вывод названия метода и результата расчета.
    print("-" * 20)
    print(f'Метод: {method.NAME}')
    print(f'Результат (S): {area:.8f}')
    print(f'Число разбиений (h): {final_interval_count}')
    print("Значение интеграла при h/2:", area2)
    print("-" * 20)


# Точка входа в программу.
if __name__ == '__main__':
    main()
