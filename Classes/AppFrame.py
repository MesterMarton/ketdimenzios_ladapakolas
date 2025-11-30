import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox

from matplotlib import pyplot as plt
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
        self.needed_bins = None

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
            text="Importált négyzetek: -"
        )
        self.imported_squares_label.pack(side=tk.TOP, anchor="w", padx=10, pady=5)

        self.choosed_algorithm_label = ttk.Label(
            self.master,
            text="Kiválasztott algoritmus: -"
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

        self.__display_bins()

        self.extra_information_label = ttk.Label(
            self.master,
            anchor="center",
            justify="center", 
            text="Ládák száma: 0 \n Szükséges ládák száma: -"
        )
        self.extra_information_label.pack(side=tk.TOP, padx=10, pady=5)

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
            text=f"Kiválasztott algoritmus: {algorithm}: {option}"
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
        # messagebox.showinfo("Indítás", "Az algoritmus elindult!")
        if self.algorithm == "heuristic":
            a = HeuristicSolver( self.squares, self.option)
            # a = HeuristicSolver([Square(5), Square(3), Square(7), Square(2), Square(6)], self.option)
            a.run()
            # self.__display_bins(a.bins)
            # print(f"Number of bins used: {len(a.bins)}")
            self.extra_information_label.config(text=f"Ládák száma: {len(a.bins)} \n Szükséges ládák száma: {self.needed_bins}")
            self.__display_bins(a.bins)

        # else if self.algorithm == "genetic":

    def __display_bins(self, bins=None):
        # Alapértékek
        bin_w = 20
        bin_h = 20
        gap = 5  # Távolság a ládák között

        # Ládák számának és elrendezésének meghatározása
        if bins is None or len(bins) == 0:
            num_bins = 0
            cols = 1
        else:
            num_bins = len(bins)
            # A kért logika:
            # 1 láda -> 1 oszlop
            # 2-4 láda -> 2 oszlop (így a 3. átkerül a 2. sorba, a 4. mellé)
            # 5+ láda -> 3 oszlop (így 9 láda 3x3-as lesz)
            if num_bins == 1:
                cols = 1
            elif num_bins <= 4:
                cols = 2
            else:
                cols = 3
        
        # Sorok számának kiszámítása
        import math
        rows = math.ceil(num_bins / cols) if num_bins > 0 else 1

        # A teljes ábra méretének kiszámítása a határok beállításához
        total_width = cols * bin_w + (cols - 1) * gap
        total_height = rows * bin_h + (rows - 1) * gap
        
        # Margó, hogy ne érjen a széléhez
        margin = 5 

        # Ha még nincs canvas / figure, hozzuk létre egyszer
        if not hasattr(self, "canvas"):
            self.plot_frame = tk.Frame(self.master)
            self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            self.fig = Figure(figsize=(6, 6))
            self.ax1 = self.fig.add_subplot(111)
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Töröljük a korábbi rajzokat
        self.ax1.cla()
        
        # Beállítjuk a határokat a rácsos elrendezéshez
        # A + margin és - margin biztosítja, hogy legyen kis keret
        self.ax1.set_xlim(-margin, total_width + margin)
        self.ax1.set_ylim(-margin, total_height + margin)
        
        self.ax1.set_aspect("equal")
        self.ax1.set_title("Ládapakolás ábrázolása:")
        
        # Y tengely fordítása, hogy a (0,0) bal felül legyen
        self.ax1.invert_yaxis()

        # Tengelyek és rács eltüntetése a tisztább képért (opcionális)
        self.ax1.axis('off') 

        base_colors = ['blue', 'green', 'orange', 'gray', 'brown', 'yellow', "red", "cyan", "magenta"]
        color_iterator = iter(base_colors)

        if bins:
            for i, bin_obj in enumerate(bins):
                # Rács pozíció kiszámítása (sor, oszlop)
                row = i // cols
                col = i % cols

                # A láda bal felső sarkának koordinátája a rácsban
                # X: oszlop * (szélesség + hézag)
                # Y: sor * (magasság + hézag)
                bin_offset_x = col * (bin_w + gap)
                bin_offset_y = row * (bin_h + gap)

                # Láda keretének kirajzolása
                bin_rect = plt.Rectangle(
                    (bin_offset_x, bin_offset_y),  
                    bin_w, bin_h,       
                    facecolor="none",  
                    edgecolor="black",
                    linewidth=2
                )
                self.ax1.add_patch(bin_rect)
                
                # Láda sorszámának kiírása (opcionális, de hasznos)
                self.ax1.text(bin_offset_x, bin_offset_y - 1, f"Bin {bin_obj.id}", fontsize=8)

                # Négyzetek kirajzolása a ládán belül
                for square in bin_obj.squares:
                    try:
                        color = next(color_iterator)
                    except StopIteration:
                        color_iterator = iter(base_colors)
                        color = next(color_iterator)
                    
                    # KOORDINÁTA KORREKCIÓ:
                    # A Square osztályban a square.x így van tárolva: local_x + (bin_id-1)*20
                    # Ezt vissza kell bontanunk, hogy megkapjuk a ládán belüli relatív X-et.
                    # Mivel a Bin osztályban az id 1-től indul (len+1), ezért:
                    linear_strip_correction = (bin_obj.id - 1) * 20
                    local_x = square.x - linear_strip_correction
                    
                    # A végső pozíció a rácsban: láda_eltolás + relatív_x
                    final_x = bin_offset_x + local_x
                    final_y = bin_offset_y + square.y

                    rect = plt.Rectangle(
                        (final_x, final_y),
                        square.size, square.size,
                        facecolor=color,
                        edgecolor="black"
                    )
                    self.ax1.add_patch(rect)

        self.canvas.draw()


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

        self.needed_bins = self.calculate_needed_bins()

        self.extra_information_label.config(
            text=f"Ládák száma: 0 \n Szükséges ládák száma: {self.needed_bins}")

    def calculate_needed_bins(self):
        if self.squares is None or len(self.squares) == 0:
            return
        total_area = sum([square.size * square.size for square in self.squares])
        needed_bins = total_area // (20 * 20)
        if total_area % (20 * 20) != 0:
            needed_bins += 1
        return needed_bins

        
    
