class Square:
    def __init__(self, size):
        self.size = size
        self.x = 0
        self.y = 0

    def set_position(self, x, y, bin_id):
        # print(bin_id)
        self.x = x + bin_id * 20 - 20
        self.y = y