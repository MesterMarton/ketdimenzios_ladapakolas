import numpy as np

# láda mérete statikus még

class Bin:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.space_matrix = np.full((20, 20), True, dtype=bool)

    # szabad hely keresése a mátrixban
    def find_empyt_place(self, square):
        size = square.size
        for i in range(self.space_matrix.shape[0] - size + 1):
            for j in range(self.space_matrix.shape[1] - size + 1):
                if np.all(self.space_matrix[i:i+size, j:j+size]):
                    self.space_matrix[i:i+size, j:j+size] = False
                    square.set_position(j, i)
                    return True
        return False
    

    # legnagybb szabadhely a mátrixban
    def largest_square(self):
        max_size = 0
        for i in range(self.space_matrix.shape[0]):
            for j in range(self.space_matrix.shape[1]):
                if self.space_matrix[i, j]:
                    size = 1
                    while (i + size < self.space_matrix.shape[0] and
                           j + size < self.space_matrix.shape[1] and
                           np.all(self.space_matrix[i:i+size+1, j:j+size+1])):
                        size += 1
                    max_size = max(max_size, size)
        return max_size