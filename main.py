import tkinter as tk
from tkinter import ttk

# Імпортуємо наш словник текстів
from lang.lang_ua import TEXTS

# Створюємо головне вікно програми
root = tk.Tk()
root.title(TEXTS["window_title"])
root.geometry("600x400")

# Створюємо рамку (контейнер) для елементів введення, щоб вони виглядали охайно
input_frame = ttk.LabelFrame(root, text=TEXTS["input_frame_title"])
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Підпис і поле вводу для лівої межі (a)
label_a = ttk.Label(input_frame, text=TEXTS["label_a"])
label_a.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entry_a = ttk.Entry(input_frame, width=10)
entry_a.insert(0, "0")  # Вставляємо початкове значення за замовчуванням
entry_a.grid(row=0, column=1, padx=5, pady=5)

# Підпис і поле вводу для правої межі (b)
label_b = ttk.Label(input_frame, text=TEXTS["label_b"])
label_b.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

entry_b = ttk.Entry(input_frame, width=10)
entry_b.insert(0, "2")  # Початкове значення
entry_b.grid(row=0, column=3, padx=5, pady=5)

# Змінна, яка буде зберігати значення обраного методу (за замовчуванням "dichotomy")
method_var = tk.StringVar(value="dichotomy")

# Створюємо перемикачі (Radiobuttons) у нашій рамці введення
radio_dichotomy = ttk.Radiobutton(input_frame, text=TEXTS["method_dichotomy"], variable=method_var, value="dichotomy")
radio_dichotomy.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_iteration = ttk.Radiobutton(input_frame, text=TEXTS["method_iteration"], variable=method_var, value="iteration")
radio_iteration.grid(row=1, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_newton = ttk.Radiobutton(input_frame, text=TEXTS["method_newton"], variable=method_var, value="newton")
radio_newton.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

# Кнопка «Розрахувати»
def on_calculate():
    # Поки що тут просто тестовий вивід обраного методу в консоль
    selected = method_var.get()
    print(f"Обрано метод: {selected}")
    print(f"Межа a: {entry_a.get()}, Межа b: {entry_b.get()}")

btn_calculate = ttk.Button(input_frame, text=TEXTS["btn_calc"], command=on_calculate)
btn_calculate.grid(row=3, column=0, columnspan=4, pady=10)





# Запускаємо безкінечний цикл відображення вікна
root.mainloop()