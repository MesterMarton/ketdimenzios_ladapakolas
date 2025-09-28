
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread

from Classes.Benchmark import Benchmark

class BenchmarkFrame(ttk.Frame):
 #   def __init__(self, container, on_data_return):
    def __init__(self, container):
        super().__init__(
            container,
            padding = (0, 0, 0, 0)
        )

      #  self.on_data_return = on_data_return

        self.bin_size_label = ttk.Label(
            self,
            text="Láda mérete:"
        )

        self.number_of_squares_label = ttk.Label(
            self,
            text="Bemeneti négyzetek száma:"
        )

        self.min_square_size_label = ttk.Label(
            self,
            text="Minimális négyzet méret:"
        )

        self.max_square_size_label = ttk.Label(
            self,
            text="Maximális négyzet méret:"
        )
        
        # Bevitelimezők létrehozása #
        self.bin_size = ttk.Entry(
            self,
            width=35
        )

        self.number_of_squares = ttk.Entry(
            self,
            width=35
        )

        self.min_square_size = ttk.Entry(
            self,
            width=35
        )

        self.max_square_size = ttk.Entry(
            self,
            width=35
        )

        # Gomb létrehozása #
        self.create_benchmark = ttk.Button(
            self,
            text="Benchmark létrehozása",
            command=self.__create_benchmark
        )

        # Elhelyezés a képernyőn #
        self.bin_size_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 10))
        self.bin_size.grid(row=1, column=1, sticky=tk.W, pady=(10, 10))
        self.number_of_squares_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 10))
        self.number_of_squares.grid(row=2, column=1, sticky=tk.W, pady=(10, 10))
        self.min_square_size_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 10))
        self.min_square_size.grid(row=3, column=1, sticky=tk.W, pady=(10, 10))
        self.max_square_size_label.grid(row=4, column=0, sticky=tk.W, pady=(10, 10))
        self.max_square_size.grid(row=4, column=1, sticky=tk.W, pady=(10, 10))
        self.create_benchmark.grid(row=9, column=0, sticky=tk.EW, pady=(10, 10), columnspan=2)

        self.pack()

    def __create_benchmark(self):

        new_benchmark = Benchmark(
            int(self.bin_size.get()),
            int(self.number_of_squares.get()),
            int(self.min_square_size.get()),
            int(self.max_square_size.get())
        )

        new_benchmark.create_folder()
        new_benchmark.create_inputs()


        # mesaurement_thread = Thread(target=lambda: self.__meres())
        # mesaurement_thread.start()
            
        # self.__monitor(mesaurement_thread)


    def choose_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Mentés ide",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path = file_path
            print("Kiválasztott mentési hely:", self.file_path)
        else:
            print("Nem lett mentési hely kiválasztva.")
