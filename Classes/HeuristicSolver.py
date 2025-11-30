import random # Szükséges az importálás
from Classes.Bin import Bin
from Classes.Square import Square

class HeuristicSolver:
    def __init__(self, squares=None, option=None):
        self.squares = squares
        self.option = option
        self.bins = []

    def sort_squares_by_size(self):
        if self.squares is not None:
            self.squares.sort(key=lambda square: square.size, reverse=True)
        else:
            raise ValueError("Squares list is not initialized.")
        
    def run(self):
        # A kiválasztott opció alapján döntünk a futtatásról
        
        # Hagyományos FFD algoritmusok
        if "FFD" in self.option:
            self.sort_squares_by_size()
            if "Top Left" in self.option:
                self.first_fit(bottom_up=False)
            elif "Bottom Left" in self.option:
                self.first_fit(bottom_up=True)
                
        # Az új "Lokális javító" (Split) algoritmusok
        elif "Split" in self.option:
            # Itt a rendezés a csoportbontás után történik
            if "Top Left" in self.option:
                self.split_and_fit(bottom_up=False)
            elif "Bottom Left" in self.option:
                self.split_and_fit(bottom_up=True)

    # Segédfüggvény egy darab négyzet elhelyezésére
    def place_square(self, square, bottom_up=False):
        placed = False
        for bin in self.bins:
            # Irány kiválasztása
            if bottom_up:
                # Feltételezve, hogy megírtad az előző lépésben a find_empty_place_bottom_left-et
                if hasattr(bin, 'find_empty_place_bottom_left'):
                    success = bin.find_empty_place_bottom_left(square)
                else:
                    # Ha nincs megírva, fallback a simára (vagy hiba)
                    success = bin.find_empty_place(square)
            else:
                success = bin.find_empty_place(square)

            if success:
                placed = True
                break
        
        # Ha egyik ládába sem fért be, újat nyitunk
        if not placed:
            new_bin = Bin(len(self.bins) + 1)
            self.bins.append(new_bin)
            if bottom_up and hasattr(new_bin, 'find_empty_place_bottom_left'):
                new_bin.find_empty_place_bottom_left(square)
            else:
                new_bin.find_empty_place(square)

    def first_fit(self, bottom_up=False):
        self.bins = [] # Biztos ami biztos, nullázzuk a ládákat
        for square in self.squares:
            self.place_square(square, bottom_up)

    # ... (a fájl eleje és többi része változatlan) ...

    def split_and_fit(self, bottom_up=False):
        # 1. Random bontás
        group1 = []
        group2 = []
        for s in self.squares:
            if random.random() < 0.5:
                group1.append(s)
            else:
                group2.append(s)
        
        self.split_log = {
            "Group 1": [s.size for s in group1],
            "Group 2": [s.size for s in group2]
        }
        
        # 2. Rendezés
        group1.sort(key=lambda s: s.size, reverse=True)
        group2.sort(key=lambda s: s.size, reverse=True)

        # 3. Újrapakolás
        self.bins = []
        for s in group1:
            self.place_square(s, bottom_up)
        for s in group2:
            self.place_square(s, bottom_up)