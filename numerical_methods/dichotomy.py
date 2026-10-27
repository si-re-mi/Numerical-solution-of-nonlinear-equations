# метод дихотомії
def f(x):
    return x**3 + x**2 - 5*x + 2

def dichotomy(a, b, eps):
    n = 0
    while (b - a) / 2 > eps:
        c = (a + b) / 2
        if (f(a) * f(c) < 0):
            b = c # звужуємо правий кінець
        else:
            a = c # звужуємо лівий кінець                       
        n = n + 1
    return (c, n)