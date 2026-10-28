import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

# Імпортуємо наш словник текстів
from lang.lang_ua import TEXTS

# Імпортуємо наші математичні методи з папки methods
from numerical_methods.dichotomy import dichotomy
from numerical_methods.iteration import iteration
from numerical_methods.newton import newtone

# Імпортуємо словник функцій для різних варіантів
from functions import VARIANTS, numerical_derivative

# Імпортуємо функції для перевірки коректності введених даних
from validators import validate_boundaries_and_domain, check_result_validity

# Імпортуємо модулі збереження та графіків
from export_utils import save_results_to_file, plot_function_graph

# Створюємо головне вікно програми
root = tk.Tk()

# Задаємо іконку програми
try:
    root.iconbitmap("feather_2.ico")
    """
    Автор Іконки: https://www.flaticon.com/ru/authors/iconixar
    """
except Exception:
    pass  # Якщо файл іконки раптом відсутній, програма не впаде, а піде далі
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

# Поле для введення власної похибки (дефолтно 0.0001)
label_eps_input = ttk.Label(input_frame, text=TEXTS["label_eps"])
label_eps_input.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

entry_eps = ttk.Entry(input_frame, width=15)
entry_eps.insert(0, "0.0001")
entry_eps.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

# Перемикачі методів
method_var = tk.StringVar(value="dichotomy")

radio_dichotomy = ttk.Radiobutton(input_frame, text=TEXTS["method_dichotomy"], variable=method_var, value="dichotomy")
radio_dichotomy.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_iteration = ttk.Radiobutton(input_frame, text=TEXTS["method_iteration"], variable=method_var, value="iteration")
radio_iteration.grid(row=4, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_newton = ttk.Radiobutton(input_frame, text=TEXTS["method_newton"], variable=method_var, value="newton")
radio_newton.grid(row=4, column=4, columnspan=2, sticky=tk.W, padx=5, pady=5)

# --- ФУНКЦІЯ РОЗРАХУНКУ ТА ДОДАВАННЯ РЯДКА ---
def on_calculate_single(clear_table=False):
    """Виконує розрахунок для заданої похибки та додає рядок у таблицю."""
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

        # Зчитуємо введену користувачем похибку
        try:
            eps = float(entry_eps.get())
            if eps <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror(TEXTS["error_eps_title"], TEXTS["error_eps_msg"])
            return
        
        selected_method = method_var.get()
        
        # Якщо потрібно очистити таблицю перед розрахунком (наприклад, при першому натисканні або повній заміні)
        if clear_table:        
            for item in tree.get_children():
                tree.delete(item)
        
        # Обчислення обраним методом
        if selected_method == "dichotomy":
            root_x, n_iter = dichotomy(a, b, eps, funcs["f"])
        elif selected_method == "iteration":
            root_x, n_iter = iteration(a, b, eps, funcs["phi"], funcs["phi_prime"])
        elif selected_method == "newton":
            root_x, n_iter = newtone(a, b, eps, funcs["f"], funcs["f_1"])
        else:
            return
        
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

def on_calculate_default_table():
    """Розраховує три стандартні похибки з методички (0.01, 0.001, 0.0001) та заповнює таблицю."""
    for item in tree.get_children():
        tree.delete(item)
    
    default_eps_values = [0.01, 0.001, 0.0001]
    for val in default_eps_values:
        entry_eps.delete(0, tk.END)
        entry_eps.insert(0, str(val))
        on_calculate_single(clear_table=False)

# Кнопка запуску розрахунку
btn_calculate = ttk.Button(input_frame, text=TEXTS["btn_calc"], command=on_calculate_default_table)
btn_calculate.grid(row=5, column=0, padx=5, pady=10, sticky=tk.EW)

# Кнопка додавання рядка з власною похибкою
btn_add_row = ttk.Button(input_frame, text=TEXTS["btn_add_eps"], command=lambda: on_calculate_single(clear_table=False))
btn_add_row.grid(row=5, column=1, padx=5, pady=10, sticky=tk.EW)

# Кнопка збереження результатів у файл
btn_save = ttk.Button(input_frame, text=TEXTS["save_btn_text"], command=lambda: save_results_to_file(tree))
btn_save.grid(row=5, column=2, padx=5, pady=10, sticky=tk.EW)

# Кнопка побудови графіка
btn_plot = ttk.Button(input_frame, text=TEXTS["plot_btn_text"], command=lambda: plot_function_graph(entry_a, entry_b, variant_combobox, entry_custom))
btn_plot.grid(row=5, column=3, padx=5, pady=10, sticky=tk.EW)

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