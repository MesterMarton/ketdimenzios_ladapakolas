import random
from pathlib import Path

class Benchmark:
    def __init__(self, S, n, a, b):
        self.BinSize = S
        self.number_of_squares = n
        self.min_square_size = a
        self.max_square_size = b
        self.file_path = Path(__file__).parent.parent/"inputs"
        self.new_folder = None

    def create_folders(self):
        self.new_folder = self.file_path / f"S{self.BinSize}_Min{self.min_square_size}_Max{self.max_square_size}_N{self.number_of_squares}"
        self.new_folder.mkdir(parents=True, exist_ok=True)

    def create_inputs(self):

        for i in range(self.number_of_squares):
            square_size = random.randint(self.min_square_size, self.max_square_size)

            with open(self.new_folder / f"input_{i+1}.txt", "w") as f:
                f.write(f"{square_size}\n")