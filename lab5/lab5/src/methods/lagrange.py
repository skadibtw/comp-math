from common import rounded
from dots import Dots
from ordered_set import OrderedSet
global lagrange_print
lagrange_print = OrderedSet()

def lagrange(dots: Dots, X: float) -> float:
    n = dots.get_n()
    xs = dots.get_xs()
    ys = dots.get_ys()  

    res = 0
    for i in range(n):
        y_i = ys[i]

        q = 1
        for j in range(n):
            if i != j:
                q *= (X - xs[j]) / (xs[i] - xs[j])
        lagrange_print.add(f"l_{i} = {q}")
        res += y_i * q

    return rounded(res)
