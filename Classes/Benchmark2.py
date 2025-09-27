import tkinter as tk
from ctypes import windll, wintypes

from Classes.SettingsFrame import SettingsFrame

class SettingsWindow(tk.Toplevel):
    # def __init__(self, parent,on_data_return):
    def __init__(self, parent):
        super().__init__(parent)
        
        windll.user32.SetThreadDpiAwarenessContext(wintypes.HANDLE(-4))
        
        self.title("Settings")
        window_width = 460
        window_height = 320
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        position_width = int(screen_width / 2 - window_width / 2)
        position_height = int(screen_height / 2 - window_height / 2)
        
        self.geometry(f"{window_width}x{window_height}+{position_width}+{position_height}")
        self.minsize(420, 300)
        
   #     SettingsFrame(self, on_data_return=on_data_return)
        SettingsFrame(self)