import tkinter as tk
from ctypes import windll, wintypes

from Classes.SettingsFrame import SettingsFrame

class SettingsWindow(tk.Toplevel):
    # def __init__(self, parent,on_data_return):
    def __init__(self, parent, on_data_return=None):
        super().__init__(parent)
        
        windll.user32.SetThreadDpiAwarenessContext(wintypes.HANDLE(-4))
        
        self.title("Beállítások")
        window_width = 460
        window_height = 320
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        position_width = int(screen_width / 2 - window_width / 2)
        position_height = int(screen_height / 2 - window_height / 2)
        
        self.geometry(f"{window_width}x{window_height}+{position_width}+{position_height}")
        self.minsize(420, 300)

        self.on_data_return = on_data_return
        
        SettingsFrame(self, on_data_return=self._on_apply)
        # SettingsFrame(self)

    def _on_apply(self, algorithm, option):
       
        if self.on_data_return:
            self.on_data_return(algorithm, option)  # átadja az adatokat az AppFrame-nek
        self.destroy()  # bezárja az ablakot