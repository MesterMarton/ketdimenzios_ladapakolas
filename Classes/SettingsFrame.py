import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread

from Classes.HeuristicSolver import HeuristicSolver

class SettingsFrame(ttk.Frame):
    def __init__(self, container, on_data_return=None):
        super().__init__(
            container,
            padding = (0, 0, 0, 0)
        )

        self.title_label = ttk.Label(
            self,
            text="Válassza ki az algoritmust:",
            font=("Arial", 12, "bold")
        )

        self.on_data_return = on_data_return
        self.title_label.pack(side=tk.TOP, anchor="w", pady=(0, 10))

        self.algorithm_var = tk.StringVar(value="heuristic")

        radio_frame = ttk.Frame(self)
        radio_frame.pack(side=tk.TOP, anchor="w", pady=5)

        self.heuristic_radio = ttk.Radiobutton(
            radio_frame,
            text="Heurisztikus algoritmus",
            variable=self.algorithm_var,
            value="heuristic",
            command=self.update_combobox
        )
        self.heuristic_radio.pack(side=tk.LEFT, padx=(0, 20)) 

        self.genetic_radio = ttk.Radiobutton(
            radio_frame,
            text="Genetikus algoritmus",
            variable=self.algorithm_var,
            value="genetic",
            command=self.update_combobox
        )
        self.genetic_radio.pack(side=tk.LEFT)

        self.combo_label = ttk.Label(self, text="Válasszon opciót:")
        self.combo_label.pack(side=tk.TOP, anchor="w", pady=(15, 5))

        self.combobox_var = tk.StringVar()
        self.combobox = ttk.Combobox(self, textvariable=self.combobox_var, state="readonly")
        self.combobox.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.apply_button = ttk.Button(self, text="Alkalmaz", command=self.on_apply)
        self.apply_button.pack(side=tk.TOP, pady=(15, 0))

        self.update_combobox()

        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_combobox(self):
        algorithm = self.algorithm_var.get()
        if algorithm == "heuristic":
            items = ["First Fit Decreasing", "Algoritmus B", "Algoritmus C"]
        else:
            items = ["Genetikus X", "Genetikus Y", "Genetikus Z"]
        self.combobox['values'] = items
        if items:
            self.combobox.current(0)

    def on_apply(self):
        print("Kiválasztott algoritmus:", self.algorithm_var.get())
        print("Kiválasztott opció a listából:", self.combobox_var.get())

        if self.on_data_return:
            self.on_data_return(self.algorithm_var.get(), self.combobox_var.get())