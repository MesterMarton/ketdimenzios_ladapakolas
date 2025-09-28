import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyparsing import Path

from Classes.HeuristicSolver import HeuristicSolver
from Classes.Square import Square
from Classes.SettingsWindow import SettingsWindow
from Classes.BenchmarkWindow import BenchmarkWindow

class AppFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(
            container,
            padding = (0, 0, 0, 0)
        )
        self.squares = None
        self.algorithm = None
        self.option = None

        self.prev_mes_menu = tk.Menu(
            self.master.menubar,
            tearoff=0
        )

        self.master.menubar.add_cascade(
            label="Fájl",
            menu=self.prev_mes_menu
        )

        self.prev_mes_menu.add_command(
            label="Új",
           # image=self.db_icon,
            compound="left",
            command = self.__create_new_benchmark,
            font=("", 9)
        )

        self.prev_mes_menu.add_command(
            label="Megnyitás",
            # image=self.file_icon,
            compound="left",
            command = self.__import_from_txt,
            font=("", 9)
        )

        self.imported_squares_label = ttk.Label(
            self.master,
            text="Importált négyzetek:"
        )
        self.imported_squares_label.pack(side=tk.TOP, anchor="w", padx=10, pady=5)

        self.choosed_algorithm_label = ttk.Label(
            self.master,
            text="Kiválasztott algoritmus:"
        )
        self.choosed_algorithm_label.pack(side=tk.TOP, anchor="w", padx=10, pady=5)
       

        self.master.menubar.add_command(
            label="Beállítások",
            command=self.__display_settings_window
        )

        self.master.menubar.add_command(
            label="Indítás",
            command=self.__run_algorithm
        )

        self.master.menubar.add_command(
            label="Leállítás",
          #   command=self.__display_instrument_window
        )

        self.master.menubar.add_command(
            label="Kilépés",
            command=self.master.destroy
        )

        self.__display_graphs()

    def __display_settings_window(self):
        settings_window = SettingsWindow(self, on_data_return=self.receive_settings_data)
        settings_window.grab_set()
        settings_window.focus()
        self.wait_window(settings_window)

    def __create_new_benchmark(self):
        benchmark_window = BenchmarkWindow(self)
        benchmark_window.grab_set()
        benchmark_window.focus()
        self.wait_window(benchmark_window)

    def receive_settings_data(self, algorithm, option):
        self.choosed_algorithm_label.config(
            text=f"Kiválasztott algoritmus: {algorithm}, Opció: {option}"
        )
        self.algorithm = algorithm
        self.option = option

    def __run_algorithm(self):
        if self.algorithm == None:
            messagebox.showwarning("Figyelmeztetés", "Nincs kiválasztva algoritmus!")
            return
        if self.squares == None or len(self.squares) == 0:
            messagebox.showwarning("Figyelmeztetés", "Nincsenek importált négyzetek!")
            return
        messagebox.showinfo("Indítás", "Az algoritmus elindult!")
        if self.algorithm == "heuristic":
            a = HeuristicSolver( self.squares, self.option)
            a.run()

        # else if self.algorithm == "genetic":

    def __display_graphs(self):

        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Egy matplotlib Figure létrehozása három subplot-tal (egy oszlopban elrendezve)
        self.fig = Figure(figsize=(8, 10))
        self.fig.tight_layout()
        self.fig.subplots_adjust(hspace=0.5)
        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)

        # 1. Grafikon: LED feszültség vs. LED áram (I-V karakterisztika)
        self.ax1.set_xlabel("LED feszültség [V]")
        self.ax1.set_ylabel("LED áram [A]")
        self.ax1.set_title("LED I-V karakterisztika")
        self.ax1.grid(True)

        # 2. Grafikon: LED feszültség vs. Detektor áram (fényintenzitás karakterisztika)
        self.ax2.set_xlabel("LED feszültség [V]")
        self.ax2.set_ylabel("Detektor áram [A]")
        self.ax2.set_title("LED fényintenzitás karakterisztika")
        self.ax2.grid(True)

        # 3. Grafikon: LED áram vs. Detektor áram
        self.ax3.set_xlabel("LED áram [A]")
        self.ax3.set_ylabel("Detektor áram [A]")
        self.ax3.set_title("LED áram - Detektor áram karakterisztika")
        self.ax3.grid(True)

        self.line1, = self.ax1.plot([], [], marker='o', linestyle='-')
        self.line2, = self.ax2.plot([], [], marker='s', color='r', linestyle='-')
        self.line3, = self.ax3.plot([], [], marker='^', color='g', linestyle='-')


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def __import_from_txt(self):
        file_path = filedialog.askopenfilename(
            initialdir=Path(__file__).parent.parent/"inputs",
            title="Import from .txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                proceed = messagebox.askyesno(
                    title="Fájl beolvasva",
                    message=f"A {file_path} fájl kiválasztása sikeres volt.\nSzeretné ezeket az adatokat betölteni?"
                )
                # Ha a felhasználó az IGEN-t nyomta
                if proceed:
                    self.create_squares(content)
                # print("A kiválasztott fájl tartalma:")
                # print(content)
                # self.convertToVisualizationFormat(content)
            except Exception as e:
                messagebox.showinfo("Error","Hiba történt a fájl beolvasása során:", e)
        # else:
        #     messagebox.showinfo("Figyelmeztetés","Nem lett fájl kiválasztva.")

    def create_squares(self, content):
        lines = content.splitlines()
        self.squares = []
        for line in lines:
            try:
                size = int(line.strip())
                if size > 0:
                    square = Square(size)
                    self.squares.append(square)
            except ValueError:
                messagebox(f"Hiba történt a betöltés során!")
        # print(f"{len(self.squares)} négyzet lett létrehozva.")
        sizes = ""
        for square in self.squares:
            sizes += f"{square.size} "
        self.imported_squares_label.config(text=f"Importált négyzetek: {sizes}")

    def convertToVisualizationFormat(self, content):
        # Az adatok feldolgozása:
        lines = content.splitlines()
        for i in lines:
            print(i)
        if len(lines) < 2:
            print("Nincs elegendő adat a megjelenítéshez!")
            return

        LEDCurrentArray = []
        LEDFeszTomb = []
        PhotoCurrentArray = []
        # print(len(lines))
        for line in lines[1:]:
            parts = line.split("\t")
            # print(len(parts))
            # if len(parts) < 4:
            #     continue
            LEDCurrentArray.append(float(parts[1]))
            LEDFeszTomb.append(float(parts[2]))
            PhotoCurrentArray.append(float(parts[3]))

            # print(float(parts[1]))
            # print(float(parts[2]))
            # print(float(parts[3]))

        if not LEDCurrentArray or not LEDFeszTomb or not PhotoCurrentArray:
            print("Nem sikerült az adatok feldolgozása!")
            return

        # # Ha esetleg már létezett korábbi grafikonokat tartalmazó frame, akkor azt töröljük
        # if hasattr(self, "plot_frame") and self.plot_frame.winfo_exists():
        #     self.plot_frame.destroy()
        self.__update_graphs(LEDFeszTomb, LEDCurrentArray, PhotoCurrentArray)