from methods.newton_div import get_newton_polynomial, newton_div
import actions
dots = actions.get_preset_function()
print(newton_div(dots, 1.5))