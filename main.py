import tkinter as tk
from tkinter import ttk

# Імпортуємо наш словник текстів
from lang.lang_ua import TEXTS

# Імпортуємо наші математичні методи з папки methods
from numerical_methods.dichotomy import dichotomy
from numerical_methods.iteration import iteration
from numerical_methods.newton import newtone

# Створюємо головне вікно програми
root = tk.Tk()
root.title(TEXTS["window_title"])
root.geometry("800x550")

# --- РЯДОК СТАНУ (Status Bar) ---
status_var = tk.StringVar()
status_var.set("Готово до роботи.")
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

# Перемикачі методів
method_var = tk.StringVar(value="dichotomy")

radio_dichotomy = ttk.Radiobutton(input_frame, text=TEXTS["method_dichotomy"], variable=method_var, value="dichotomy")
radio_dichotomy.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_iteration = ttk.Radiobutton(input_frame, text=TEXTS["method_iteration"], variable=method_var, value="iteration")
radio_iteration.grid(row=1, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

radio_newton = ttk.Radiobutton(input_frame, text=TEXTS["method_newton"], variable=method_var, value="newton")
radio_newton.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

# --- ФУНКЦІЯ РОЗРАХУНКУ ТА ЗАПОВНЕННЯ ТАБЛИЦІ ---
def on_calculate():
    try:
        status_var.set(TEXTS["status_calculating"])
        
        # Отримуємо введені користувачем межі та обраний метод
        a = float(entry_a.get())
        b = float(entry_b.get())
        selected_method = method_var.get()
        
        # Очищуємо таблицю від старих результатів перед новим розрахунком
        for item in tree.get_children():
            tree.delete(item)
            
        # Вимоги лабораторної: обчислення для трьох значень похибки
        eps_values = [0.01, 0.001, 0.0001]
        
        for eps in eps_values:
            # Викликаємо відповідну функцію залежно від вибору
            if selected_method == "dichotomy":
                root_x, n_iter = dichotomy(a, b, eps)
            elif selected_method == "iteration":
                root_x, n_iter = iteration(a, b, eps)
            elif selected_method == "newton":
                root_x, n_iter = newtone(a, b, eps)
                
            # Обчислюємо значення функції в знайденій точці
            func_val = root_x**3 + root_x**2 - 5*root_x + 2
            
            # Додаємо рядок у таблицю Treeview
            tree.insert("", tk.END, values=(str(eps), str(n_iter), f"{root_x:.6f}", f"{func_val:.6f}"))
            
        status_var.set(TEXTS["status_done"])
        
    except Exception as e:
        messagebox.showerror(TEXTS["error_title"], f"{TEXTS['error_message']}{str(e)}")
        status_var.set("Помилка обчислення.")


# Кнопка запуску розрахунку
btn_calculate = ttk.Button(input_frame, text=TEXTS["btn_calc"], command=on_calculate)
btn_calculate.grid(row=3, column=0, columnspan=4, pady=10)


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