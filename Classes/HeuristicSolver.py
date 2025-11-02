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
     #   print("Selected algorithm:", self.option)
        if self.option == "FFD - Top Left":
            self.first_fit()

    def first_fit(self):
        for square in self.squares:
            placed = False
            for bin in self.bins:
                if bin.find_empty_place(square):
                    placed = True
                    break
            if not placed:
                new_bin = Bin(len(self.bins) + 1)
                self.bins.append(new_bin)
                new_bin.find_empty_place(square)

# h = HeuristicSolver([Square(5), Square(3), Square(7), Square(2), Square(6)], "first_fit")
# h.run()
# print(f"Number of bins used: {len(h.bins)}")
