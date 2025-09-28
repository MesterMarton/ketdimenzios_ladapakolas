from Classes.Square import Square

class HeuristicSolver:
    def __init__(self, squares=None, option = None):
        self.squares = squares
        self.option = option

    def sort_squares_by_size(self):
        if self.squares is not None:
            self.squares.sort(key=lambda square: square.size, reverse=True)
        else:
            raise ValueError("Squares list is not initialized.")
        
    def run(self):
        print("Ide eljut")
        self.sort_squares_by_size()
        print("Heurisztikus algoritmus fut...")
       
