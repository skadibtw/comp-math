from sympy import diff
import math

def derr_phi(x):
    return -math.sin(x)
def iter_method(f, phi, x0, eps, a, b, max_iterations=1000):
    x = x0
    h = 1e-6  # шаг для численной дифференциации
    #derr_phi = lambda x_val: (phi(x_val + h) - phi(x_val - h)) / (2 * h)

    if abs(derr_phi(a)) > 1 or abs(derr_phi(b)) > 1:
        print(f"Метод, вероятнее всего, не сойдется, так как |phi'(a)| = {abs(derr_phi(a))}, |phi'(b)| = {abs(derr_phi(b))}")
    print(
        f"phi'(a)| = {abs(derr_phi(a))}, |phi'(b)| = {abs(derr_phi(b))}")

    for i in range(max_iterations):
        x_new = phi(x)
        if abs(x_new - x) <= eps:
            return x_new, f(x_new), i + 1
        x = x_new
    raise ValueError("Iterations > max")
