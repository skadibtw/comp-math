def bisection_method(f, a, b, eps, max_iter=1000):
    if f(a) * f(b) > 0:
        raise ValueError("Функция должна иметь разные знаки на концах отрезка.")
    for i in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < eps or abs(b - a) < eps:
            print("Длина интервала стала", b-a)
            return c, f(c), i + 1
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    raise ValueError("Превышено число итераций.")
