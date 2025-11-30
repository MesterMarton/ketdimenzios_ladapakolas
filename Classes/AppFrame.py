import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path

from Classes.HeuristicSolver import HeuristicSolver
from Classes.Square import Square
from Classes.SettingsWindow import SettingsWindow
from Classes.BenchmarkWindow import BenchmarkWindow

class AppFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.pack(fill=tk.BOTH, expand=True) # A Frame töltse ki az ablakot

        # --- ADATOK ---
        self.squares = None
        self.algorithm = None
        self.option = None
        self.needed_bins = None

        # --- STÍLUSOK DEFINIÁLÁSA ---
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        self.style.configure("Card.TLabelframe", background="#f0f0f0")
        self.style.configure("Card.TLabelframe.Label", font=("Segoe UI", 10, "bold"), foreground="#333")

        # --- MENÜ LÉTREHOZÁSA ---
        self._create_menu()

        # --- FŐ ELRENDEZÉS (Layout) ---
        # Két részre osztjuk: Bal oldal (Sidebar) és Jobb oldal (Content)
        
        self.main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 1. BAL OLDAL (Sidebar)
        self.sidebar = ttk.Frame(self.main_paned, width=250, padding=(0, 0, 10, 0))
        self.main_paned.add(self.sidebar, weight=1)

        # 2. JOBB OLDAL (Main Content - Grafikon)
        self.content_area = ttk.Frame(self.main_paned, padding=(10, 0, 0, 0))
        self.main_paned.add(self.content_area, weight=4)

        # --- SIDEBAR TARTALMA ---
        
        # Cím
        self.title_label = ttk.Label(self.sidebar, text="Ládapakolás", style="Header.TLabel")
        self.title_label.pack(side=tk.TOP, anchor="w", pady=(0, 20))

        # Adatok kártya
        # ... (előző kódok: info_frame létrehozása) ...

        # Adatok kártya
        self.info_frame = ttk.LabelFrame(self.sidebar, text="Bemeneti adatok", style="Card.TLabelframe", padding=10)
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # TÖRÖLTÜK a fix 'wraplength=200'-at
        self.imported_squares_label = ttk.Label(self.info_frame, text="Nincs adat betöltve", justify="left")
        self.imported_squares_label.pack(anchor="w", fill=tk.X)

        # EZ AZ ÚJ SOR: Ha változik a keret mérete, frissítse a sortörést
        self.info_frame.bind("<Configure>", lambda e: self.imported_squares_label.config(wraplength=self.info_frame.winfo_width()-20))
        # Algoritmus kártya
        self.algo_frame = ttk.LabelFrame(self.sidebar, text="Algoritmus", style="Card.TLabelframe", padding=10)
        self.algo_frame.pack(fill=tk.X, pady=5)

        self.choosed_algorithm_label = ttk.Label(self.algo_frame, text="Nincs kiválasztva", wraplength=200)
        self.choosed_algorithm_label.pack(anchor="w")

        # Eredmény kártya
       # Eredmény kártya (Statisztika)
        self.stats_frame = ttk.LabelFrame(self.sidebar, text="Statisztika", style="Card.TLabelframe", padding=10)
        self.stats_frame.pack(fill=tk.X, pady=5)

        # 1. TÖRÖLTÜK a 'wraplength=200'-at innen is
        # 2. Hozzáadtuk a 'fill=tk.X'-et a pack-hez, hogy kitöltse a teret
        self.extra_information_label = ttk.Label(self.stats_frame, text="Futtatásra vár...", justify="left")
        self.extra_information_label.pack(anchor="w", fill=tk.X)

        # 3. ÚJ SOR: Dinamikus tördelés figyelése (ugyanaz, mint a fentinél)
        self.stats_frame.bind("<Configure>", lambda e: self.extra_information_label.config(wraplength=self.stats_frame.winfo_width()-20))

        # --- TARTALOM TERÜLET (Grafikon) ---
        # Kezdetben kirajzoljuk az üres táblát
        self.__display_bins()

    def _create_menu(self):
        self.prev_mes_menu = tk.Menu(self.master.menubar, tearoff=0)
        self.master.menubar.add_cascade(label="Fájl", menu=self.prev_mes_menu)
        self.prev_mes_menu.add_command(label="Új Benchmark", command=self.__create_new_benchmark)
        self.prev_mes_menu.add_command(label="Megnyitás (.txt)", command=self.__import_from_txt)

        self.master.menubar.add_command(label="Beállítások", command=self.__display_settings_window)
        self.master.menubar.add_command(label="Indítás", command=self.__run_algorithm)
        self.master.menubar.add_command(label="Javítás", command=self.__run_repair) # Javítás gomb
        self.master.menubar.add_command(label="Kilépés", command=self.master.destroy)

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
        # Csak a nevét írjuk ki szépen
        self.choosed_algorithm_label.config(text=f"{algorithm}\n({option})")
        self.algorithm = algorithm
        self.option = option

    def __run_algorithm(self):
        if self.algorithm is None:
            messagebox.showwarning("Figyelmeztetés", "Nincs kiválasztva algoritmus!")
            return
        if self.squares is None or len(self.squares) == 0:
            messagebox.showwarning("Figyelmeztetés", "Nincsenek importált négyzetek!")
            return

        if self.algorithm == "heuristic":
            # Stratégia meghatározása az opció szövegéből
            strategy = "TopLeft"
            if "Bottom Left" in str(self.option):
                strategy = "BottomLeft"
            elif "Corners" in str(self.option):
                strategy = "Corners"

            a = HeuristicSolver(self.squares, self.option)
            a.run()
            
            self._update_stats_ui(a, strategy)
            self.__display_bins(a.bins)

    def __run_repair(self):
        if self.algorithm is None:
            messagebox.showwarning("Figyelmeztetés", "Előbb válassz algoritmust és futtasd le!")
            return
        if self.squares is None or len(self.squares) == 0:
            messagebox.showwarning("Figyelmeztetés", "Nincsenek négyzetek betöltve!")
            return

        # Stratégia meghatározása a legutolsó beállítás alapján
        strategy = "TopLeft"
        strategy_lbl = "Bal-Felső"
        if "Bottom Left" in str(self.option):
            strategy = "BottomLeft"
            strategy_lbl = "Bal-Alsó"
        elif "Corners" in str(self.option):
            strategy = "Corners"
            strategy_lbl = "4 Sarok"

        if self.algorithm == "heuristic":
            a = HeuristicSolver(self.squares, self.option)
            a.split_and_fit(strategy=strategy)
            
            self._update_stats_ui(a, strategy_lbl, is_repair=True)
            self.__display_bins(a.bins)

    def _update_stats_ui(self, solver_instance, strategy_name, is_repair=False):
        # Külön függvény a statisztika frissítésére, hogy ne duplikáljuk a kódot
        info_text = f"Felhasznált ládák: {len(solver_instance.bins)}\n Szükséges ládák (min): {self.needed_bins}"

        if hasattr(solver_instance, 'split_log') and solver_instance.split_log:
            g1_str = ", ".join(map(str, solver_instance.split_log["Group 1"]))
            g2_str = ", ".join(map(str, solver_instance.split_log["Group 2"]))
            prefix = "JAVÍTÁS" if is_repair else "SPLIT"
            info_text += f"\n\n--- {prefix} ADATOK ---\nMód: {strategy_name}\n\n1. Csoport ({len(solver_instance.split_log['Group 1'])} db):\n{g1_str}\n\n2. Csoport ({len(solver_instance.split_log['Group 2'])} db):\n{g2_str}"
        
        self.extra_information_label.config(text=info_text)


    def __display_bins(self, bins=None):
        # --- BEÁLLÍTÁSOK ---
        bin_w = 20
        bin_h = 20
        gap = 2       # CSÖKKENTETT HÉZAG (5 helyett 2), hogy közelebb legyenek
        margin = 2    # CSÖKKENTETT MARGÓ (5 helyett 2)

        # Oszlopok és sorok számítása
        if bins is None or len(bins) == 0:
            num_bins = 0
            cols = 1
        else:
            num_bins = len(bins)
            if num_bins == 1:
                cols = 1
            elif num_bins <= 4:
                cols = 2
            else:
                cols = 3
        
        import math
        rows = math.ceil(num_bins / cols) if num_bins > 0 else 1
        total_width = cols * bin_w + (cols - 1) * gap
        total_height = rows * bin_h + (rows - 1) * gap

        # Ha még nincs canvas, létrehozzuk
        if not hasattr(self, "canvas"):
            # !!! ITT A VÁLTOZÁS: figsize=(8, 8) az (5, 5) helyett !!!
            # Ez jelentősen megnöveli az ábra méretét
            self.fig = Figure(figsize=(8, 8), dpi=100) 
            self.fig.patch.set_facecolor('#f0f0f0')
            self.ax1 = self.fig.add_subplot(111)
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.content_area)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ax1.cla()
        
        # Nézet beállítása
        if bins is None:
            self.ax1.text(total_width/2, total_height/2, "Várakozás az adatokra...", 
                          horizontalalignment='center', verticalalignment='center', color='gray')
            self.ax1.set_xlim(0, 40)
            self.ax1.set_ylim(0, 40)
        else:
            self.ax1.set_xlim(-margin, total_width + margin)
            self.ax1.set_ylim(-margin, total_height + margin)
        
        self.ax1.set_aspect("equal")
        self.ax1.invert_yaxis()
        self.ax1.axis('off') 

        base_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        color_iterator = iter(base_colors)

        if bins:
            for i, bin_obj in enumerate(bins):
                row = i // cols
                col = i % cols
                bin_offset_x = col * (bin_w + gap)
                bin_offset_y = row * (bin_h + gap)

                # Láda keret
                bin_rect = plt.Rectangle((bin_offset_x, bin_offset_y), bin_w, bin_h, facecolor="white", edgecolor="#333", linewidth=1.5)
                self.ax1.add_patch(bin_rect)
                self.ax1.text(bin_offset_x, bin_offset_y - 1, f"Láda {bin_obj.id}", fontsize=9, color="#555", weight="bold")

                for square in bin_obj.squares:
                    try:
                        color = next(color_iterator)
                    except StopIteration:
                        color_iterator = iter(base_colors)
                        color = next(color_iterator)
                    
                    linear_strip_correction = (bin_obj.id - 1) * 20
                    local_x = square.x - linear_strip_correction
                    final_x = bin_offset_x + local_x
                    final_y = bin_offset_y + square.y

                    rect = plt.Rectangle((final_x, final_y), square.size, square.size, facecolor=color, edgecolor="black", alpha=0.9)
                    self.ax1.add_patch(rect)
                    
                    # Méret kiírása - most már kicsit nagyobb betűvel, ha elfér
                    if square.size >= 3:
                        font_size = 7 if square.size < 5 else 9 # Nagyobb betűk nagyobb négyzetekbe
                        self.ax1.text(final_x + square.size/2, final_y + square.size/2, str(square.size), 
                                      ha='center', va='center', fontsize=font_size, color='white', weight='bold')

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

                proceed = messagebox.askyesno(title="Fájl beolvasva", message=f"Szeretné betölteni az adatokat?")
                if proceed:
                    self.create_squares(content)
            except Exception as e:
                messagebox.showinfo("Error", f"Hiba történt: {e}")

    def create_squares(self, content):
        lines = content.splitlines()
        self.squares = []
        try:
            for line in lines:
                val = line.strip()
                if val:
                    size = int(val)
                    if size > 0:
                        self.squares.append(Square(size))
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen fájlformátum!")
            return

        sizes_str = ", ".join([str(s.size) for s in self.squares])
        
        # Most már a TELJES listát kiírjuk, nem vágjuk le 50 karakternél
        self.imported_squares_label.config(text=f"{len(self.squares)} db elem:\n{sizes_str}")

        self.needed_bins = self.calculate_needed_bins()
        self.extra_information_label.config(text=f"Szükséges ládák (min): {self.needed_bins}\n\nFuttatásra kész.")

    def calculate_needed_bins(self):
        if self.squares is None or len(self.squares) == 0:
            return 0
        total_area = sum([square.size * square.size for square in self.squares])
        needed_bins = total_area // (20 * 20)
        if total_area % (20 * 20) != 0:
            needed_bins += 1
        return needed_bins