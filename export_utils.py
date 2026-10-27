# export_utils.py
import math
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from lang.lang_ua import TEXTS
from functions import VARIANTS

def save_results_to_file(tree):
    """Зберігає поточні дані з таблиці Treeview у текстовий файл з урахуванням локалізації."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")],
        title=TEXTS["save_file_title"]
    )
    if not file_path:
        return
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{TEXTS['file_header_title']}\n")
            f.write("-" * 65 + "\n")
            f.write(f"{TEXTS['col_eps_file']:<18} | {TEXTS['col_iter_file']:<15} | {TEXTS['col_root_file']:<18} | {TEXTS['col_func_file']:<18}\n")
            f.write("-" * 65 + "\n")
            
            for item in tree.get_children():
                vals = tree.item(item, "values")
                f.write(f"{vals[0]:<18} | {vals[1]:<15} | {vals[2]:<18} | {vals[3]:<18}\n")
                
        messagebox.showinfo(TEXTS["save_success_title"], TEXTS["save_success_msg"])
    except Exception as e:
        messagebox.showerror(TEXTS["save_error_title"], f"{str(e)}")

def plot_function_graph(entry_a, entry_b, variant_combobox, entry_custom):
    """Будує графік функції на відрізку [a, b] з урахуванням обраного варіанта чи власного рівняння."""
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        selected_variant = variant_combobox.get()
        
        # Визначаємо функцію залежно від обраного у випадаючому списку варіанта
        if selected_variant == TEXTS["custom_variant_name"]:
            custom_str = entry_custom.get()
            f_to_plot = lambda x: eval(custom_str, {
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
        else:
            f_to_plot = VARIANTS[selected_variant]["f"]
            
        # Генеруємо точки для графіка
        x_vals = np.linspace(a, b, 400)
        y_vals = [f_to_plot(val) for val in x_vals]
        
        # Побудова графіка за допомогою matplotlib
        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_vals, label="f(x)", color="#1f77b4", linewidth=2)
        plt.axhline(0, color="black", linewidth=1, linestyle="--")
        plt.title(f"{TEXTS['table_frame_title']}: {selected_variant}")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True, linestyle=":", alpha=0.7)
        plt.legend()
        plt.show()
        
    except Exception as e:
        messagebox.showerror(TEXTS["plot_error_title"], f"{str(e)}")