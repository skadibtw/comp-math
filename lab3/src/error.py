from typing import Any


# Печатает сообщение об ошибке и завершает программу с кодом 1.
def print_error_and_exit(message: Any) -> None:
    print(message)
    exit(1)
