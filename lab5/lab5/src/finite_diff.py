from types import NoneType
from common import rounded
from dots import Dots


def get_finite_diffs(dots: Dots) -> list[list[float | str]]:
    n = dots.get_n()
    xs = dots.get_xs()
    ys = dots.get_ys()
    
    # теперь n строк и n+1 колонка: x, y, Δy, Δ²y, …
    result = [['' for _ in range(n + 1)] for _ in range(n)]
    
    for i in range(n):
        result[i][0] = xs[i]
        result[i][1] = ys[i]
    
    # конечные разности: для порядка k=1…n-1 пишем в колонку k+1
    for k in range(1, n):
        for j in range(0, n - k):
            result[j][k + 1] = rounded(result[j + 1][k] - result[j][k])
    return result
