# validators.py
import math
from tkinter import messagebox
from lang.lang_ua import TEXTS

def validate_boundaries_and_domain(selected_variant, a, b):
    """
    Перевіряє межі відрізка [a, b] на відповідність області визначення обраного рівняння.
    Повертає True, якщо все гаразд, або False (і виводить попередження), якщо є порушення.
    """
    # 1. Перевірка для логарифмів (аргумент має бути > 0)
    if ("ln" in selected_variant or "log" in selected_variant) and (a <= 0 or b <= 0):
        messagebox.showwarning(
            TEXTS["warn_domain_title"],
            TEXTS["warn_log_message"]
        )
        return False

    # 2. Перевірка загальної коректності меж (межа 'a' має бути меншою за 'b')
    if a >= b:
        messagebox.showwarning(
            TEXTS["warn_bounds_title"],
            TEXTS["warn_bounds_message"]
        )
        return False

    return True

def check_result_validity(root_x):
    """
    Перевіряє, чи є знайдений корінь дійсним числом.
    """
    if math.isnan(root_x) or math.isinf(root_x):
        raise ValueError(TEXTS["error_not_converged"])