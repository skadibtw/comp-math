def newton_method_systems(func, jacobian, x0, tol=1e-6, max_iter=1000):
    x = list(x0)
    iter_count = 0

    while True:
        f_x = func(x)
        jacobian_x = jacobian(x)
        delta_x = [0, 0]
        det_j = jacobian_x[0][0] * jacobian_x[1][1] - jacobian_x[0][1] * jacobian_x[1][0]
        if det_j == 0:
            print("Детерминант якобиана равен нулю. Метод Ньютона не может быть применен.")
            return None, iter_count
        
        # Вычисляем обратный якобиан
        inv_jacobian_x = [jacobian_x[1][1] / det_j, -jacobian_x[0][1] / det_j,
                          -jacobian_x[1][0] / det_j, jacobian_x[0][0] / det_j]
        # Вычисляем изменение переменных
        delta_x[0] = -(inv_jacobian_x[0] * f_x[0] + inv_jacobian_x[1] * f_x[1])
        delta_x[1] = -(inv_jacobian_x[2] * f_x[0] + inv_jacobian_x[3] * f_x[1])
        # (Δx, Δy) = - J⁻¹(x, y) · (f(x, y), g(x, y)).
        x_new = [xi + dxi for xi, dxi in zip(x, delta_x)]
        iter_count += 1

        if (abs(x_new[0] - x[0]) < tol or abs(x_new[1] - x[1]) < tol) or iter_count >= max_iter:
            x = x_new
            break
        x = x_new

    return x, iter_count
