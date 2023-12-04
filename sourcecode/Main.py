import tkinter as tk
from tkinter import ttk
from gui import BiometricSystem

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background='#3498db', foreground='white', width=20, borderwidth=1, focusthickness=3,
                    focuscolor='none')
    style.map('TButton', background=[('active', '#3498db')])
    app = BiometricSystem(root)
    root.mainloop()