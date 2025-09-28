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
        if self.option == "first_fit":
            self.first_fit()

    def first_fit(self):
       bin = Bin("Bin1", 0)
       self.bins
       for square in self.squares:
           if not(bin.find_empyt_place(square)):
                bin = Bin(f"Bin{len(self.bins)+1}", 0)
                bin.find_empyt_place(square)
