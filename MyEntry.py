import tkinter as tk
from config import ent_font, red


class MyEntry(tk.Entry):
    def __init__(self, master):
        super(MyEntry, self).__init__(master, width=6, font=ent_font, borderwidth=3)

    # функція для валідації введених даних
    def check(self):
        try:
            float(self.get())
            return True
        except ValueError:
            self.config(bg=red)
            self.delete(0, 'end')
            self.insert(0, '0')
            return False
