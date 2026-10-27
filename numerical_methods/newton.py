# метод Ньютона (дотичних)
def find_initial_approximation(a, b, f_1):
    """
    Автоматично обирає безпечну початкову точку на відрізку [a, b]
    для методу Ньютона, щоб уникнути ділення на нуль або розбіжності.
    """
    try:
        # Перевіряємо лівий кінець (a)
        if f_1(a) != 0:
            return a
        # Перевіряємо правий кінець (b)
        elif f_1(b) != 0:
            return b
    except (ZeroDivisionError, ValueError):
        pass
        
    # Якщо на кінцях похідна нульова чи виникає помилка, беремо середину
    return (a + b) / 2

def newtone(a, b, eps, f, f_1):
    """
    Знаходить корінь рівняння методом Ньютона (дотичних).
    Приймає межі відрізка [a, b] та похибку eps.
    Повертає знайдений корінь та кількість ітерацій.
    """
    # Автоматично обираємо безпечну початкову точку
    x_old = find_initial_approximation(a, b, f_1)

    # Захист, якщо раптом перша точка дає нульову похідну
    derivative = f_1(x_old)
    if derivative == 0:
        x_old += 0.01
        derivative = f_1(x_old)
        
    x_new = x_old - (f(x_old) / derivative)
    n = 1
    while abs(x_new - x_old) > eps:
        x_old = x_new
        # Захист від ділення на нуль під час ітерацій
        if f_1(x_old) == 0:
            break
        x_new = x_old - (f(x_old) / f_1(x_old))                   
        n = n + 1
    return (x_new, n)