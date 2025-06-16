def secant_method(f, a, b, eps, max_iter=1000):
    if f(a) * f(b) > 0:
        raise ValueError("Функция должна иметь разные знаки на концах отрезка.")
    x0 = (a+b)/2  # Начальное приближение
    x1 = x0 + eps  # Второе приближение
    for i in range(max_iter):
        try:
            x = x1 - ((x1 - x0) / (f(x1) - f(x0))) * f(x1)
        except ValueError:
            raise ValueError("Ошибка в вычислении функции.")
        except ZeroDivisionError:
            raise ValueError("Деление на ноль в методе секущих.")
        if abs(x - x1) < eps or abs(f(x)) < eps:
            return x, f(x), i + 1
        x0 = x1
        x1 = x

    raise ValueError("Превышено число итераций.")
