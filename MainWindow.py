import tkinter as tk
import tkinter.messagebox as mb

from MyEntry import MyEntry
from config import rb_font, bt_font, txt_font, bg_color, white, green, greeting_text
from SettingsWindow import SettingsWindow
from Matrix import Matrix


# Клас, який відповідає за функціонал і візуал програми
class MainWindow(tk.Tk):
    def __init__(self, title='Пошук власних чисел і векторів', resizable=False, order=2):
        super().__init__()
        self.title(title)
        self.resizable(width=resizable, height=resizable)
        self.iconbitmap(r'C:\Users\user\PycharmProjects\Curse4\resource\pic.ico')
        self.config(padx=15, pady=15, bg=bg_color)

        self.__choice = tk.IntVar()
        self.__order = order
        self.__entries = list()
        self.__matrix = list()

        try:
            open('results.txt', 'w').close()
        except:
            pass

        self.__text = tk.Text()

    def create_workspace(self, matrix=False):
        frame1 = tk.Frame(self, bg=bg_color)
        frame1.grid(row=0, column=0, stick='wn')

        for i in range(self.__order):
            temp = list()
            for j in range(self.__order):
                ent = MyEntry(frame1)
                if matrix:
                    ent.insert(0, str(matrix[i][j]))
                else:
                    ent.insert(0, '0')
                ent.grid(row=i, column=j, pady=2, padx=2)
                temp.append(ent)
            self.__entries.append(temp)




        frame2 = tk.Frame(self, bg=bg_color)
        frame2.grid(row=2, column=0, stick='sw', rowspan=2)

        save_to_file_button = tk.Button(frame2, text='Зберегти умову', command=self.save_to_file_click)
        save_to_file_button.grid(stick='w',row=1, column=0)

        read_from_file_button = tk.Button(frame2, text='Зчитати умову', command=self.read_from_file_click)
        read_from_file_button.grid(stick='w',row=1, column=1)

        label = tk.Label(frame2, text="Метод: ", font=('montserrat', 23, 'bold'), bg=bg_color)
        label.grid(row=0, column=0)

        self.__choice = tk.IntVar()
        self.__choice.set(1)
        tk.Radiobutton(frame2, text='Данилевського', font=rb_font, bg=bg_color, variable=self.__choice, value=1).grid(
            row=0, column=1, padx=5, pady=10)
        tk.Radiobutton(frame2, text='Обертань', font=rb_font, bg=bg_color, variable=self.__choice, value=2).grid(
            row=0, column=2, padx=5)
        self.__text = tk.Text(height=17, width=35, font=txt_font)
        self.__text.insert('1.0', greeting_text)
        self.__text.config(state='disabled')
        self.__text.grid(row=0, column=1)

        solve_button = tk.Button(text='Старт', font=bt_font, bg=green, height=1, width=3, borderwidth=3,
                                 command=self.__start_button_click)
        solve_button.grid(row=1, column=1, stick='we')
        settings_button = tk.Button(text='Змінити порядок матриці', font=bt_font, height=1, width=3, borderwidth=3,
                                    command=self.__settings_button_click)
        settings_button.grid(row=2, column=1, stick='we')

    def start(self):
        self.create_workspace()
        self.mainloop()

    def restart(self, order, matrix=False):
        self.__order = order
        self.__entries.clear()
        [i.destroy() for i in self.winfo_children()]
        self.create_workspace(matrix)

    def __settings_button_click(self):
        settings = SettingsWindow(self)
        settings.grab_set()

    def save_to_file_click(self):
        with open('start_data.txt', 'w', encoding='utf-16') as ouf:
            ouf.write(str(len(self.__matrix))+'\n')
            matrix = str()
            for i in self.__matrix:
                for j in i:
                    matrix += str(j) + ' '
                matrix += '\n'
            ouf.write(matrix)

    def read_from_file_click(self):
        with open('start_data.txt', 'r', encoding='utf-16') as inf:
            text = inf.readlines()
            order = int(text[0][0])
            matrix = list()
            for i in range(1, len(text)):
                temp = list()
                for j in text[i].split():
                    temp.append(j)
                matrix.append(temp)
            self.restart(order, matrix)

    # обробка натиснення кнопки "Старт"
    def __start_button_click(self):
        self.__text.config(state='normal')
        self.__text.delete('1.0', 'end')
        status = self.__get_matrix()
        if not status:
            self.__text.config(state='disabled')
            for i in self.__entries:
                for j in i:
                    j.config(bg=white)
            return
        result = 'Виникла помилка! :('
        if self.__choice.get() == 1:
            if Matrix(self.__matrix).isMatrixDiagonal():
                result = ([self.__matrix[i][i] for i in range(self.__order)],
                          [[(1 if i == j else 0) for i in range(self.__order)] for j in range(self.__order)])
                result = Matrix(self.__matrix).special_case_format(result)
            else:
                result = Matrix(self.__matrix).danylevskyy_method()
                if not result:
                    mb.showerror(title='Під час обчислень виникла помилка!',
                                 message='Найбільш вірогідно, що під час обчислень виникла вироджена матриця.')
                    return
                temp_result = Matrix(self.__matrix).format_danilevskiy_results(result)
                self.__text.insert('1.0', temp_result)
                mb.showinfo('Кількість ітерацій', message=f'Обчислення виконано за {str(result[3])} ітерацій')
                self.__save_to_file(self.__matrix, temp_result)
                self.__text.config(state='disabled')
                if Matrix(self.__matrix).draw(result[2]):
                    pass
                else:
                    mb.showinfo(title='Помилка',
                                message="Коренями полінома є комплексні числа, ми не можемо пубудувати точний графік")
                return
        if self.__choice.get() == 2:
            if Matrix(self.__matrix).isMatrixSymmetric():
                if Matrix(self.__matrix).isMatrixDiagonal():
                    result = ([self.__matrix[i][i] for i in range(self.__order)],
                              [[(1 if i == j else 0) for i in range(self.__order)] for j in range(self.__order)])
                    result = Matrix(self.__matrix).special_case_format(result)
                else:
                    result = Matrix(self.__matrix).rotate_method(eps=1e-9)
                    mb.showinfo(title='Кількість ітерацій', message=f'Обчислення виконано за{str(result[2])} ітерацій')
                    result = Matrix(self.__matrix).format_rotation_results(result)
            else:
                mb.showerror('Error', 'Матриця не є симетричною')
        self.__text.insert('1.0', result)
        self.__save_to_file(self.__matrix, result)
        self.__text.config(state='disabled')

    def __get_matrix(self):
        flag = True
        self.__matrix.clear()
        for i in range(self.__order):
            temp = list()
            for j in range(self.__order):
                if self.__entries[i][j].check():
                    temp.append(float(self.__entries[i][j].get()))
                else:
                    flag = False
            self.__matrix.append(temp)
        if flag:
            return True
        else:
            mb.showerror(title='Помилка', message='Некоректні дані')
            return False



    @staticmethod
    def __save_to_file(start_matrix, text):
        matrix = 'Вхідна матриця\n==========\n'
        for i in start_matrix:
            for j in i:
                matrix += str(j) + ' '
            matrix += '\n'
        matrix += '===========\n'
        with open('results.txt', 'a', encoding='utf-16') as ouf:
            ouf.write(matrix)
            ouf.write(text)
