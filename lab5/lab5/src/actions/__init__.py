from .custom import get_custom_function
from .presets import get_preset_function
from input import read_dots_from_file

ACTIONS = [
    {'name': 'Ввести вручную',       'func': get_custom_function},
    {'name': 'Считать из файла',     'func': read_dots_from_file},
    {'name': 'Выбрать из пресетов',  'func': get_preset_function},
]
