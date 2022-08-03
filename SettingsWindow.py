import tkinter as tk
from config import *


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, title='Налаштування', resizable=False):
        super().__init__(parent)
        self.__parent = parent
        self.title(title)
        self.resizable(width=resizable, height=resizable)
        self.config(padx=20, pady=20, bg=bg_color)
        self.iconbitmap(r'C:\Users\user\PycharmProjects\Curse4\resource\pic.ico')

        self.__order = tk.IntVar()
        self.__order.set(2)

        __label = tk.Label(self, text="Порядок матриці", font=('comic sans ms', 23, 'bold'), bg=bg_color)
        __label.grid(row=0, column=0, columnspan=7)

        tk.Radiobutton(self, text='2', font=rb_font, bg=bg_color, variable=self.__order, value=2).grid(row=1, column=0,
                                                                                                       padx=5, pady=10)
        tk.Radiobutton(self, text='3', font=rb_font, bg=bg_color, variable=self.__order, value=3).grid(row=1, column=1,
                                                                                                       padx=5)
        tk.Radiobutton(self, text='4', font=rb_font, bg=bg_color, variable=self.__order, value=4).grid(row=1, column=2,
                                                                                                       padx=5)
        tk.Radiobutton(self, text='5', font=rb_font, bg=bg_color, variable=self.__order, value=5).grid(row=1, column=3,
                                                                                                       padx=5)
        tk.Radiobutton(self, text='6', font=rb_font, bg=bg_color, variable=self.__order, value=6).grid(row=1, column=4,
                                                                                                       padx=5)
        tk.Radiobutton(self, text='7', font=rb_font, bg=bg_color, variable=self.__order, value=7).grid(row=1, column=5,
                                                                                                       padx=5)
        tk.Radiobutton(self, text='8', font=rb_font, bg=bg_color, variable=self.__order, value=8).grid(row=1, column=6,
                                                                                                       padx=5)

        tk.Button(self, text='Зберегти', font=bt_font, height=1, width=3, borderwidth=3,
                  command=self.start_button_click).grid(row=2, column=0, columnspan=3, stick='we')
        tk.Button(self, text='Вийти', font=bt_font, borderwidth=3, command=self.destroy).grid(row=2, column=4,
                                                                                              columnspan=3, stick='we')

    def start_button_click(self):
        self.__parent.restart(self.__order.get())

