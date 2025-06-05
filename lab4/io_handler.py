import os

BASE_DIR = os.path.dirname(__file__)
# Путь к файлу по умолчанию, можно изменить при необходимости
DEFAULT_FILE_IN = os.path.join(BASE_DIR, "iofiles", "input.txt")

def getdata_file(filepath=DEFAULT_FILE_IN):
    """ Получить данные из файла """
    dots = []
    try:
        with open(filepath, 'rt', encoding='UTF-8') as fin:
            for line in fin:
                # Пропускаем пустые строки или строки с комментариями (начинающиеся с #)
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) != 2:
                    print(f"Предупреждение: Некорректный формат строки в файле: '{line}'. Пропускается.")
                    continue
                try:
                    current_dot = tuple(map(float, parts))
                    dots.append(current_dot)
                except ValueError:
                    print(f"Предупреждение: Не удалось преобразовать строку в числа: '{line}'. Пропускается.")
                    continue

        if len(dots) < 2:
            print("Ошибка: В файле должно быть как минимум 2 корректные точки.")
            return None
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {filepath}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

    return {'dots': dots}


def getdata_input():
    """ Получить данные с клавиатуры """
    dots = []
    print("\nВводите координаты (X Y) через пробел, каждая точка с новой строки.")
    print("Минимум 2 точки. Чтобы закончить, введите 'END' или 'end'.")
    while True:
        try:
            current = input(f"Точка {len(dots) + 1}: ").strip()
            if current.upper() == 'END':
                if len(dots) < 2:
                    print("Ошибка: Необходимо ввести как минимум 2 точки.")
                    # Продолжаем ввод, не выходим
                    continue
                break # Выход из цикла, если точек достаточно

            parts = current.split()
            if len(parts) != 2:
                raise ValueError("Необходимо ввести ровно два числа (X и Y).")

            current_dot = tuple(map(float, parts))
            dots.append(current_dot)

        except ValueError as e:
            print(f"Ошибка ввода: {e}. Пожалуйста, введите точку повторно.")
        except Exception as e: # Ловим другие возможные ошибки
            print(f"Произошла ошибка: {e}. Попробуйте еще раз.")

    return {'dots': dots}
