import numpy as np

# láda mérete statikus még
class Bin:
    def __init__(self, id):
        self.id = id
        self.squares = []
        self.space_matrix = np.full((20, 20), True, dtype=bool)

    # szabad hely keresése a mátrixban
    def find_empty_place(self, square):
        size = square.size
        for i in range(self.space_matrix.shape[0] - size + 1):
            for j in range(self.space_matrix.shape[1] - size + 1):
                if np.all(self.space_matrix[i:i+size, j:j+size]):
                    self.space_matrix[i:i+size, j:j+size] = False
                    square.set_position(j, i, self.id)
                    self.squares.append(square)
                    return True
        return False
    
    # szabad hely keresése lentről felfelé (Bottom-Left)
    def find_empty_place_bottom_left(self, square):
        size = square.size
        start_row = self.space_matrix.shape[0] - size
        for i in range(start_row, -1, -1):
            for j in range(self.space_matrix.shape[1] - size + 1):
                if np.all(self.space_matrix[i:i+size, j:j+size]):
                    self.space_matrix[i:i+size, j:j+size] = False
                    square.set_position(j, i, self.id)
                    self.squares.append(square)
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
    
    # ... (importok és osztály definíció) ...

    # Szabad hely keresése a 4 sarokból indulva befelé
    def find_empty_place_corners(self, square):
        size = square.size
        rows = self.space_matrix.shape[0]
        cols = self.space_matrix.shape[1]
        
        # Lehetséges bal-felső koordináták határai
        valid_rows = rows - size + 1
        valid_cols = cols - size + 1
        
        # Az összes lehetséges (sor, oszlop) pozíció generálása
        positions = []
        for i in range(valid_rows):
            for j in range(valid_cols):
                positions.append((i, j))
        
        # A 4 sarok koordinátái (ahová a négyzet sarka kerülne)
        # Bal-Felső (i=0, j=0)
        # Jobb-Felső (i=0, j=max)
        # Bal-Alsó (i=max, j=0)
        # Jobb-Alsó (i=max, j=max)
        max_r = valid_rows - 1
        max_c = valid_cols - 1
        corners = [(0, 0), (0, max_c), (max_r, 0), (max_r, max_c)]
        
        # Távolságfüggvény: a legközelebbi saroktól való Manhattan távolság
        def dist_to_nearest_corner(pos):
            r, c = pos
            # Megnézzük a távolságot mind a 4 saroktól, és a legkisebbet vesszük
            dists = [abs(r - cr) + abs(c - cc) for cr, cc in corners]
            return min(dists)
            
        # Rendezés: a legkisebb távolságú (sarkok) legyenek elöl
        positions.sort(key=dist_to_nearest_corner)
        
        # Beillesztés a rendezett sorrend szerint
        for i, j in positions:
            if np.all(self.space_matrix[i:i+size, j:j+size]):
                self.space_matrix[i:i+size, j:j+size] = False
                square.set_position(j, i, self.id)
                self.squares.append(square)
                return True
        return False
    
    # def write_space_matrix(self):
    #     for row in self.space_matrix:
    #         print(' '.join(['1' if cell else '0' for cell in row]))
    #     print()