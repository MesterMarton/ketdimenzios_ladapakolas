from Classes.Bin import Bin
from Classes.Square import Square

class HeuristicSolver:
    def __init__(self, squares=None, option = None):
        self.squares = squares
        self.option = option
        self.bins = []

    def sort_squares_by_size(self):
        if self.squares is not None:
            self.squares.sort(key=lambda square: square.size, reverse=True)
        else:
            raise ValueError("Squares list is not initialized.")
        
    def run(self):
        self.sort_squares_by_size()
        
        # Itt választjuk szét a két logikát
        if self.option == "FFD - Top Left":
            self.first_fit(bottom_up=False)
        elif self.option == "FFD - Bottom Left":
            self.first_fit(bottom_up=True)

    def first_fit(self, bottom_up=False):
        for square in self.squares:
            placed = False
            for bin in self.bins:
                # Ha bottom_up igaz, akkor az új keresőt használjuk
                if bottom_up:
                    success = bin.find_empty_place_bottom_left(square)
                else:
                    success = bin.find_empty_place(square)
                
                if success:
                    placed = True
                    break
            
            if not placed:
                new_bin = Bin(len(self.bins) + 1)
                self.bins.append(new_bin)
                # Az új ládában is a megfelelő irány szerint keresünk
                if bottom_up:
                    new_bin.find_empty_place_bottom_left(square)
                else:
                    new_bin.find_empty_place(square)

# h = HeuristicSolver([Square(5), Square(3), Square(7), Square(2), Square(6)], "first_fit")
# h.run()
# print(f"Number of bins used: {len(h.bins)}")
