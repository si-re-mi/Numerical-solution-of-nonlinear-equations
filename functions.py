import math
from lang.lang_ua import TEXTS

def numerical_derivative(f, h=1e-5):
    """
    Універсальна функція для обчислення першої похідної методом скінченних різниць.
    Використовується для методу Ньютона та перевірки умов ітерацій.
    """
    return lambda x: (f(x + h) - f(x - h)) / (2 * h)

# Словник усіх варіантів з методички (Група 1 та Група 2)
VARIANTS = {
    # --- КОРИСТУВАЦЬКИЙ ВАРІАНТ ---
    TEXTS["custom_variant_name"]: {
        "f": None,
        "phi": None,
        "f_1": None,
        "phi_prime": None
    },
    # --- ГРУПА ЗАВДАНЬ 1 ---
    "Група 1 №1: x³ + x² - 5x + 2 = 0": {
        "f": lambda x: x**3 + x**2 - 5*x + 2,
        "phi": lambda x: (x**3 + x**2 + 2) / 5
    },
    "Група 1 №2: 2x - ln(x) - 4 = 0": {
        "f": lambda x: 2*x - math.log(x) - 4 if x > 0 else float('inf'),
        "phi": lambda x: (math.log(x) + 4) / 2 if x > 0 else 0
    },
    "Група 1 №3: 10ln(x) = x³ - 3": {
        "f": lambda x: x**3 - 10*math.log(x) - 3 if x > 0 else float('inf'),
        "phi": lambda x: (10*math.log(x) + 3)**(1/3) if (10*math.log(x) + 3) >= 0 else 0
    },
    "Група 1 №4: x * tanh(x) = 1": {
        "f": lambda x: x * math.tanh(x) - 1,
        "phi": lambda x: 1 / math.tanh(x) if math.tanh(x) != 0 else 0
    },
    "Група 1 №5 & №9: x² - sin(5x) = 0": {
        "f": lambda x: x**2 - math.sin(5*x),
        "phi": lambda x: math.sqrt(math.sin(5*x)) if math.sin(5*x) >= 0 else 0
    },
    "Група 1 №6: cot(x) = 1/x - x/2": {
        "f": lambda x: (1 / math.tan(x)) - (1 / x) + (x / 2) if math.tan(x) != 0 and x != 0 else float('inf'),
        "phi": lambda x: x - 2 * ((1 / math.tan(x)) - (1 / x)) if math.tan(x) != 0 and x != 0 else 0
    },
    "Група 1 №7: e^x + e^(-3x) = 4": {
        "f": lambda x: math.exp(x) + math.exp(-3*x) - 4,
        "phi": lambda x: math.log(4 - math.exp(-3*x)) if (4 - math.exp(-3*x)) > 0 else 0
    },
    "Група 1 №8: cos(x) * cosh(x) = 1": {
        "f": lambda x: math.cos(x) * math.cosh(x) - 1,
        "phi": lambda x: math.acos(1 / math.cosh(x)) if abs(1 / math.cosh(x)) <= 1 else 0
    },
    "Група 1 №10: x + √x + x^(1/3) + x^(1/4) = 5": {
        "f": lambda x: x + math.sqrt(x) + x**(1/3) + x**(1/4) - 5 if x >= 0 else float('inf'),
        "phi": lambda x: 5 - (math.sqrt(x) + x**(1/3) + x**(1/4)) if x >= 0 else 0
    },
    "Група 1 №11: 1.8x² - sin(10x) = 0": {
        "f": lambda x: 1.8*x**2 - math.sin(10*x),
        "phi": lambda x: math.sqrt(math.sin(10*x) / 1.8) if math.sin(10*x) >= 0 else 0
    },
    "Група 1 №12: 3x - cos(x) = 1": {
        "f": lambda x: 3*x - math.cos(x) - 1,
        "phi": lambda x: (math.cos(x) + 1) / 3
    },
    "Група 1 №13: 10x = e^(-x)": {
        "f": lambda x: 10*x - math.exp(-x),
        "phi": lambda x: math.exp(-x) / 10
    },
    "Група 1 №14: x^x + 5x = 1000": {
        "f": lambda x: x**x + 5*x - 1000 if x > 0 else float('inf'),
        "phi": lambda x: (1000 - x**x) / 5 if x > 0 else 0
    },
    "Група 1 №15: ln((x+1)/(x-1)) = 2x": {
        "f": lambda x: math.log((x+1)/(x-1)) - 2*x if (x+1)/(x-1) > 0 and abs(x) > 1 else float('inf'),
        "phi": lambda x: math.log((x+1)/(x-1)) / 2 if (x+1)/(x-1) > 0 and abs(x) > 1 else 0
    },
    "Група 1 №16: e^x * sin(x) = x + 2": {
        "f": lambda x: math.exp(x) * math.sin(x) - x - 2,
        "phi": lambda x: math.exp(x) * math.sin(x) - 2
    },
    "Група 1 №17: ln(5x - 3) = 0.1x(1 + x)": {
        "f": lambda x: math.log(5*x - 3) - 0.1*x*(1 + x) if 5*x - 3 > 0 else float('inf'),
        "phi": lambda x: math.exp(0.1*x*(1 + x)) + 0.6 if 5*x - 3 > 0 else 0
    },
    "Група 1 №18: cos((x²-2)/(3x+1)) = x² - 1.5": {
        "f": lambda x: math.cos((x**2 - 2) / (3*x + 1)) - x**2 + 1.5 if (3*x + 1) != 0 else float('inf'),
        "phi": lambda x: math.sqrt(math.cos((x**2 - 2) / (3*x + 1)) + 1.5) if (3*x + 1) != 0 else 0
    },
    "Група 1 №19: (x² - 3.6x) * ln(1/x) = 1.3": {
        "f": lambda x: (x**2 - 3.6*x) * math.log(1/x) - 1.3 if x > 0 else float('inf'),
        "phi": lambda x: 3.6 + 1.3 / (x * math.log(1/x)) if x > 0 and math.log(1/x) != 0 else 0
    },
    "Група 1 №20: log((x²+2)/(x-1)) = 2": {
        "f": lambda x: math.log10((x**2 + 2) / (x - 1)) - 2 if x > 1 else float('inf'),
        "phi": lambda x: math.sqrt(10**2 * (x - 1) - 2) if x > 1 else 0
    },

    # --- ГРУПА ЗАВДАНЬ 2 ---
    "Група 2 №1: x³ + 12x² + 44x + 48 = 0": {
        "f": lambda x: x**3 + 12*x**2 + 44*x + 48,
        "phi": lambda x: -(12*x**2 + 44*x + 48)**(1/3) if (12*x**2 + 44*x + 48) >= 0 else -((-12*x**2 - 44*x - 48)**(1/3))
    },
    "Група 2 №2: x = cos(...)": {
        "f": lambda x: x - math.cos((0.7854 - x*math.sqrt(1 - x**2)) / (1 - 2*x**2)) if abs(x) <= 1 and (1 - 2*x**2) != 0 else float('inf'),
        "phi": lambda x: math.cos((0.7854 - x*math.sqrt(1 - x**2)) / (1 - 2*x**2)) if abs(x) <= 1 and (1 - 2*x**2) != 0 else 0
    },
    "Група 2 №3: x + e^x = 0": {
        "f": lambda x: x + math.exp(x),
        "phi": lambda x: -math.exp(x)
    },
    "Група 2 №4: 4x = 7sin(x)": {
        "f": lambda x: 4*x - 7*math.sin(x),
        "phi": lambda x: 7 * math.sin(x) / 4
    },
    "Група 2 №5: 2^x = 4x": {
        "f": lambda x: 2**x - 4*x,
        "phi": lambda x: 2**(x - 2)
    },
    "Група 2 №6: cos(x) = x": {
        "f": lambda x: math.cos(x) - x,
        "phi": lambda x: math.cos(x)
    },
    "Група 2 №7: x³ - 3x² - 12x - 10 = 0": {
        "f": lambda x: x**3 - 3*x**2 - 12*x - 10,
        "phi": lambda x: (3*x**2 + 12*x + 10)**(1/3)
    },
    "Група 2 №8: 10x = e^(x - x²)": {
        "f": lambda x: 10*x - math.exp(x - x**2),
        "phi": lambda x: math.exp(x - x**2) / 10
    },
    "Група 2 №9: x^x + ln(x) = 100": {
        "f": lambda x: x**x + math.log(x) - 100 if x > 0 else float('inf'),
        "phi": lambda x: (100 - math.log(x))**(1/x) if x > 0 and (100 - math.log(x)) > 0 else 0
    },
    "Група 2 №10: ln((1+x²)/(1-x²)) = 1 - x": {
        "f": lambda x: math.log((1 + x**2) / (1 - x**2)) - 1 + x if abs(x) < 1 else float('inf'),
        "phi": lambda x: 1 - math.log((1 + x**2) / (1 - x**2)) if abs(x) < 1 else 0
    },
    "Група 2 №11: x + lg(x) = 0.5": {
        "f": lambda x: x + math.log10(x) - 0.5 if x > 0 else float('inf'),
        "phi": lambda x: 0.5 - math.log10(x) if x > 0 else 0
    },
    "Група 2 №12: x * ln(x) = 18": {
        "f": lambda x: x * math.log(x) - 18 if x > 0 else float('inf'),
        "phi": lambda x: 18 / math.log(x) if x > 0 and math.log(x) != 0 else 0
    },
    "Група 2 №13: 1 - x = sin(x/25) + x²/25": {
        "f": lambda x: 1 - x - math.sin(x/25) - (x**2)/25,
        "phi": lambda x: 1 - math.sin(x/25) - (x**2)/25
    },
    "Група 2 №14: x⁸ - 3x⁴ + 2x = 1": {
        "f": lambda x: x**8 - 3*x**4 + 2*x - 1,
        "phi": lambda x: (1 + 3*x**4 - x**8) / 2
    },
    "Група 2 №15: 2x - ln(x) = 4": {
        "f": lambda x: 2*x - math.log(x) - 4 if x > 0 else float('inf'),
        "phi": lambda x: (math.log(x) + 4) / 2 if x > 0 else 0
    },
    "Група 2 №16: x - 1 = tan((x²+5)/(x-5))": {
        "f": lambda x: x - 1 - math.tan((x**2 + 5) / (x - 5)) if x != 5 else float('inf'),
        "phi": lambda x: 1 + math.tan((x**2 + 5) / (x - 5)) if x != 5 else 0
    },
    "Група 2 №17: x³ - 3.6x² - 7.96x + 10.56 = 5sin(2x)": {
        "f": lambda x: x**3 - 3.6*x**2 - 7.96*x + 10.56 - 5*math.sin(2*x),
        "phi": lambda x: (3.6*x**2 + 7.96*x - 10.56 + 5*math.sin(2*x))**(1/3) if (3.6*x**2 + 7.96*x - 10.56 + 5*math.sin(2*x)) >= 0 else 0
    },
    "Група 2 №18: sin(x) + tan((2-x)/(x²+1)) = 0": {
        "f": lambda x: math.sin(x) + math.tan((2 - x) / (x**2 + 1)),
        "phi": lambda x: x + math.sin(x) + math.tan((2 - x) / (x**2 + 1))
    },
    "Група 2 №19: x³ = 15cos(x) - 4": {
        "f": lambda x: x**3 - 15*math.cos(x) + 4,
        "phi": lambda x: (15*math.cos(x) - 4)**(1/3) if (15*math.cos(x) - 4) >= 0 else -((-15*math.cos(x) + 4)**(1/3))
    },
    "Група 2 №20: (5x² - 3)sin(x) = 1": {
        "f": lambda x: (5*x**2 - 3) * math.sin(x) - 1,
        "phi": lambda x: math.sqrt((1 / math.sin(x) + 3) / 5) if math.sin(x) != 0 and (1 / math.sin(x) + 3) >= 0 else 0
    }
}

# Автоматичне додавання похідних (f_1 та phi_prime) для кожного варіанта за допомогою чисельного диференціювання
for name, data in VARIANTS.items():
    f_func = data["f"]
    phi_func = data["phi"]
    data["f_1"] = numerical_derivative(f_func)
    data["phi_prime"] = numerical_derivative(phi_func)