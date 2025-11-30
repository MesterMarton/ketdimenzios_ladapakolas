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
        
    # ... (HeuristicSolver osztály eleje) ...

    def run(self):
        self.sort_squares_by_size()
        
        # Stratégia meghatározása az opció szövegéből
        strategy = "TopLeft" # Alapértelmezett
        if "Bottom Left" in self.option:
            strategy = "BottomLeft"
        elif "Corners" in self.option:
            strategy = "Corners"
            
        # Algoritmus futtatása
        if "FFD" in self.option:
            self.first_fit(strategy=strategy)
        elif "Split" in self.option: # Ha a split benne maradt a kódban
            self.split_and_fit(strategy=strategy)

    # Segédfüggvény egy darab négyzet elhelyezésére
    def place_square(self, square, strategy="TopLeft"):
        placed = False
        for bin in self.bins:
            success = False
            # Stratégia kiválasztása
            if strategy == "BottomLeft":
                if hasattr(bin, 'find_empty_place_bottom_left'):
                    success = bin.find_empty_place_bottom_left(square)
                else:
                    success = bin.find_empty_place(square)
            elif strategy == "Corners":
                if hasattr(bin, 'find_empty_place_corners'):
                    success = bin.find_empty_place_corners(square)
                else:
                    success = bin.find_empty_place(square)
            else: # TopLeft
                success = bin.find_empty_place(square)

            if success:
                placed = True
                break
        
        # Ha egyik ládába sem fért be, újat nyitunk
        if not placed:
            new_bin = Bin(len(self.bins) + 1)
            self.bins.append(new_bin)
            
            # Az új ládában is a stratégiának megfelelően keresünk
            if strategy == "BottomLeft":
                new_bin.find_empty_place_bottom_left(square)
            elif strategy == "Corners":
                new_bin.find_empty_place_corners(square)
            else:
                new_bin.find_empty_place(square)

    def first_fit(self, strategy="TopLeft"):
        self.bins = []
        for square in self.squares:
            self.place_square(square, strategy=strategy)

    def split_and_fit(self, strategy="TopLeft"):
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
            self.place_square(s, strategy=strategy)
        for s in group2:
            self.place_square(s, strategy=strategy)