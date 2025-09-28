
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread

# from Classes.Measurement import Measurement

class SettingsFrame(ttk.Frame):
 #   def __init__(self, container, on_data_return):
    def __init__(self, container):
        super().__init__(
            container,
            padding = (0, 0, 0, 0)
        )

        self.title_label = ttk.Label(
            self,
            text="Válassza ki az algoritmust:",
            font=("Arial", 12, "bold")
        )
        self.title_label.pack(side=tk.TOP, anchor="w", pady=(0, 10))

        # --- Választó változó ---
        self.algorithm_var = tk.StringVar(value="heuristic")  # alapértelmezett: heuristics

        # --- Frame a rádiógomboknak ---
        radio_frame = ttk.Frame(self)
        radio_frame.pack(side=tk.TOP, anchor="w", pady=5)

        # --- Rádiógombok mellé ---
        self.heuristic_radio = ttk.Radiobutton(
            radio_frame,
            text="Heurisztikus algoritmus",
            variable=self.algorithm_var,
            value="heuristic",
            command=self.update_combobox
        )
        self.heuristic_radio.pack(side=tk.LEFT, padx=(0, 20))  # kis távolság a gombok között

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

        # --- Gomb ---
        self.apply_button = ttk.Button(self, text="Alkalmaz", command=self.on_apply)
        self.apply_button.pack(side=tk.TOP, pady=(15, 0))

        # --- Első feltöltés ---
        self.update_combobox()

        # Automatikus pack
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_combobox(self):
        algorithm = self.algorithm_var.get()
        if algorithm == "heuristic":
            items = ["Algoritmus A", "Algoritmus B", "Algoritmus C"]
        else:
            items = ["Genetikus X", "Genetikus Y", "Genetikus Z"]

        self.combobox['values'] = items
        if items:
            self.combobox.current(0)

    # --- Gomb esemény ---
    def on_apply(self):
        print("Kiválasztott algoritmus:", self.algorithm_var.get())
        print("Kiválasztott opció a listából:", self.combobox_var.get())

        # --- Automatikus pack a frame-be ---
       #  self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
      #  self.on_data_return = on_data_return

    #     Címkék létrehozása #
    #     self.led_nyitofesz_label = ttk.Label(
    #         self,
    #         text="LED Nyitófeszültség (V):"
    #     )

    #     self.led_nyitoaram_label = ttk.Label(
    #         self,
    #         text="LED Kezdeti Nyitóárama (A):"
    #     )

    #     self.led_vegso_aram_label = ttk.Label(
    #         self,
    #         text="LED Végső Nyitóárama (A):"
    #     )

    #     self.led_lepes_label = ttk.Label(
    #         self,
    #         text="LED Lépésköz (A):"
    #     )

    #     self.meresi_ido_label = ttk.Label(
    #         self,
    #         text="Két mérés között eltelt idő (s):"
    #     )

    #     self.fajl_label = ttk.Label(
    #         self,
    #         text="Mérés fájl elérési útja és fájlnév:"
    #     )
        
    #     Bevitelimezők létrehozása #
    #     self.led_nyitofesz_entry = ttk.Entry(
    #         self,
    #         width=35
    #     )

    #     self.led_nyitoaram_entry = ttk.Entry(
    #         self,
    #         width=35
    #     )

    #     self.led_vegso_aram_entry = ttk.Entry(
    #         self,
    #         width=35
    #     )

    #     self.led_lepes_entry = ttk.Entry(
    #         self,
    #         width=35
    #     )

    #     self.meresi_ido_entry = ttk.Entry(
    #         self,
    #         width=35
    #     )

    #     self.save_btn = ttk.Button(self, text="...", command=self.choose_file)

    #     self.fajl_entry = ttk.Entry(
    #         self,
    #         width=35
    #     )

    #     Gomb létrehozása #
    #     self.meres_button = ttk.Button(
    #         self,
    #         text="Mérés indítása",
    #         command=self.__start_mesaurement
    #     )

    #     Elhelyezés a képernyőn #
    #     self.led_nyitofesz_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 10))
    #     self.led_nyitofesz_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 10))
    #     self.led_nyitoaram_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 10))
    #     self.led_nyitoaram_entry .grid(row=2, column=1, sticky=tk.W, pady=(10, 10))
    #     self.led_vegso_aram_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 10))
    #     self.led_vegso_aram_entry.grid(row=3, column=1, sticky=tk.W, pady=(10, 10))
    #     self.led_lepes_label.grid(row=4, column=0, sticky=tk.W, pady=(10, 10))
    #     self.led_lepes_entry.grid(row=4, column=1, sticky=tk.W, pady=(10, 10))
    #     self.meresi_ido_label.grid(row=5, column=0, sticky=tk.W, pady=(10, 10))
    #     self.meresi_ido_entry.grid(row=5, column=1, sticky=tk.W, pady=(10, 10))
    #     self.fajl_label.grid(row=8, column=0, sticky=tk.W, pady=(10, 10))
    #     self.save_btn.grid(row=8, column=1, sticky=tk.W, pady=(10, 10))
    #     self.meres_button.grid(row=9, column=0, sticky=tk.EW, pady=(10, 10), columnspan=2)

    #     self.pack()

    #     self.file_path = None

    # def __monitor(self, thread):
    #     if thread.is_alive():
    #         self.after(100, lambda: self.__monitor(thread))

    # def __meres(self):
    #     led_nyitofesz = float(self.led_nyitofesz_entry.get())
    #     led_nyitoaram = float(self.led_nyitoaram_entry.get())
    #     led_vegso_aram = float(self.led_vegso_aram_entry.get())
    #     led_lepes = float(self.led_lepes_entry.get())
    #     meresi_ido = float(self.meresi_ido_entry.get())
    #     fajl = self.fajl_entry.get()
    #     result = [led_nyitofesz,led_nyitoaram,led_vegso_aram,led_lepes,meresi_ido,self.file_path]
    #     self.on_data_return(result)
    #     meres = Meres()
    #     self.create_measurement(led_nyitofesz,led_nyitoaram,led_vegso_aram,led_lepes,meresi_ido)
        

    # def create_measurement(self, led_nyitofesz,led_nyitoaram,led_vegso_aram,led_lepes,meresi_ido):

    #     adatok osszegyujtese
    #    self.on_data_return(list(led_nyitofesz,led_nyitoaram,led_vegso_aram,led_lepes,meresi_ido))
    #     meres = Meres()
    #     # print(self.file_path)
    #     meres.meres(led_nyitofesz, led_nyitoaram, led_vegso_aram, led_lepes, meresi_ido, self.file_path)

    # def __start_mesaurement(self):
    #     mesaurement_thread = Thread(target=lambda: self.__meres())
    #     mesaurement_thread.start()
            
    #     self.__monitor(mesaurement_thread)


    # def choose_file(self):
    #     file_path = filedialog.asksaveasfilename(
    #         title="Mentés ide",
    #         defaultextension=".txt",
    #         filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    #     )
    #     if file_path:
    #         self.file_path = file_path
    #         print("Kiválasztott mentési hely:", self.file_path)
    #     else:
    #         print("Nem lett mentési hely kiválasztva.")
