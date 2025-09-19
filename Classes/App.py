import tkinter as tk
from ctypes import windll, wintypes

from Classes.AppFrame import AppFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        windll.user32.SetThreadDpiAwarenessContext(wintypes.HANDLE(-4))
        
        self.title("LED karakterizáció")
        window_width = 1000
        window_height = 800

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        position_width = int(screen_width / 2 - window_width / 2)
        position_height = int(screen_height / 2 - window_height / 2)
        
        self.geometry(f"{window_width}x{window_height}+{position_width}+{position_height}")
        self.minsize(980, 780)

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        AppFrame(self)