import math
from functions import numerical_derivative

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Імпортуємо наш словник текстів
from lang.lang_ua import TEXTS

# Імпортуємо наші математичні методи з папки methods
from numerical_methods.dichotomy import dichotomy
from numerical_methods.iteration import iteration
from numerical_methods.newton import newtone

# Імпортуємо словник функцій для різних варіантів
from functions import VARIANTS

# Імпортуємо функції для перевірки коректності введених даних
from validators import validate_boundaries_and_domain, check_result_validity

# Створюємо головне вікно програми
root = tk.Tk()
root.title(TEXTS["window_title"])
root.geometry("800x550")

# --- РЯДОК СТАНУ (Status Bar) ---
status_var = tk.StringVar()
status_var.set(TEXTS["status_ready"])
status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# --- ФОРМА ВВЕДЕННЯ ДАНИХ ---
input_frame = ttk.LabelFrame(root, text=TEXTS["input_frame_title"])
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Поле для межі a
label_a = ttk.Label(input_frame, text=TEXTS["label_a"])
label_a.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_a = ttk.Entry(input_frame, width=10)
entry_a.insert(0, "0")
entry_a.grid(row=0, column=1, padx=5, pady=5)

# Поле для межі b
label_b = ttk.Label(input_frame, text=TEXTS["label_b"])
label_b.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
entry_b = ttk.Entry(input_frame, width=10)
entry_b.insert(0, "2")
entry_b.grid(row=0, column=3, padx=5, pady=5)

# --- ВИБІР ВАРІАНТА (РІВНЯННЯ) ---
label_variant = ttk.Label(input_frame, text=TEXTS["label_variant"])
label_variant.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

variant_combobox = ttk.Combobox(input_frame, values=list(VARIANTS.keys()), width=45, state="readonly")
variant_combobox.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)
variant_combobox.current(0)  # Встановлюємо перший варіант за замовчуванням

# Поле для введення власного рівняння
label_custom = ttk.Label(input_frame, text=TEXTS["label_custom_func"])
label_custom.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

entry_custom = ttk.Entry(input_frame, width=45)
entry_custom.insert(0, "x**3 - 5*x + 2")
entry_custom.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

# Перемикачі методів
method_var = tk.StringVar(value="dichotomy")

radio_dichotomy = ttk.Radiobutton(input_frame, text=TEXTS["method_dichotomy"], variable=method_var, value="dichotomy")
radio_dichotomy.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_iteration = ttk.Radiobutton(input_frame, text=TEXTS["method_iteration"], variable=method_var, value="iteration")
radio_iteration.grid(row=3, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_newton = ttk.Radiobutton(input_frame, text=TEXTS["method_newton"], variable=method_var, value="newton")
radio_newton.grid(row=3, column=4, columnspan=2, sticky=tk.W, padx=5, pady=5)

# --- ФУНКЦІЯ РОЗРАХУНКУ ТА ЗАПОВНЕННЯ ТАБЛИЦІ ---
def on_calculate():
    try:
        # Усередині функції розрахунку:
        selected_variant = variant_combobox.get()

        # Перевіряємо, чи обрано власний варіант
        if selected_variant == TEXTS["custom_variant_name"]:
            custom_str = entry_custom.get()
            try:
                # Створюємо безпечну лямбда-функцію з підтримкою модуля math
                f_custom = lambda x, expr=custom_str: eval(expr, {
                    "__builtins__": {}, 
                    "x": x, 
                    "math": math, 
                    "sin": math.sin, 
                    "cos": math.cos, 
                    "tan": math.tan, 
                    "log": math.log, 
                    "exp": math.exp, 
                    "sqrt": math.sqrt, 
                    "tanh": math.tanh, 
                    "cosh": math.cosh
                })
                
                # Завдяки чисельному диференціюванню похідні для Ньютона та ітерацій створюються автоматично!
                funcs = {
                    "f": f_custom,
                    "phi": lambda x: x - 0.1 * f_custom(x),  # базовий ітераційний зсув
                    "f_1": numerical_derivative(f_custom),
                    "phi_prime": numerical_derivative(lambda x: x - 0.1 * f_custom(x))
                }
            except Exception as e:
                messagebox.showerror(TEXTS["error_expr_title"], f"{TEXTS['error_expr_message']}{str(e)}")
                status_var.set("Помилка у формулі.")
                return
        else:
            funcs = VARIANTS[selected_variant]

        status_var.set(TEXTS["status_calculating"])
        
        # Отримуємо введені користувачем межі та обраний метод
        a = float(entry_a.get())
        b = float(entry_b.get())

        # --- ВИКОРИСТОВУЄМО ВАЛІДАТОР ---
        if not validate_boundaries_and_domain(selected_variant, a, b):
            status_var.set(TEXTS["status_validation_error"])
            return

        selected_method = method_var.get()
        
        # Очищуємо таблицю від старих результатів перед новим розрахунком
        for item in tree.get_children():
            tree.delete(item)
            
        # Вимоги лабораторної: обчислення для трьох значень похибки
        eps_values = [0.01, 0.001, 0.0001]
        
        for eps in eps_values:
            # Передаємо функції у методи:
            if selected_method == "dichotomy":
                root_x, n_iter = dichotomy(a, b, eps, funcs["f"])
            elif selected_method == "iteration":
                root_x, n_iter = iteration(a, b, eps, funcs["phi"], funcs["phi_prime"])
            elif selected_method == "newton":
                root_x, n_iter = newtone(a, b, eps, funcs["f"], funcs["f_1"])

            # Перевірка валідності результату
            check_result_validity(root_x)

            # Значення функції для таблиці:
            func_val = funcs["f"](root_x)
            
            # Додаємо рядок у таблицю Treeview
            tree.insert("", tk.END, values=(str(eps), str(n_iter), f"{root_x:.6f}", f"{func_val:.6f}"))
            
        status_var.set(TEXTS["status_done"])
        
    except Exception as e:
        messagebox.showerror(TEXTS["error_title"], f"{TEXTS['error_message']}{str(e)}")
        status_var.set(TEXTS["status_calc_error"])


# Кнопка запуску розрахунку
btn_calculate = ttk.Button(input_frame, text=TEXTS["btn_calc"], command=on_calculate)
btn_calculate.grid(row=5, column=0, columnspan=4, pady=10)

# --- ТАБЛИЦЯ РЕЗУЛЬТАТІВ (Treeview) ---
result_frame = ttk.LabelFrame(root, text=TEXTS["table_frame_title"])
result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

columns = ("eps", "iterations", "root", "func_val")
tree = ttk.Treeview(result_frame, columns=columns, show="headings")

tree.heading("eps", text=TEXTS["col_eps"])
tree.heading("iterations", text=TEXTS["col_iter"])
tree.heading("root", text=TEXTS["col_root"])
tree.heading("func_val", text=TEXTS["col_func"])

# Налаштування розмірів стовпців
tree.column("eps", width=120, anchor=tk.CENTER)
tree.column("iterations", width=140, anchor=tk.CENTER)
tree.column("root", width=180, anchor=tk.CENTER)
tree.column("func_val", width=180, anchor=tk.CENTER)

tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

root.mainloop()