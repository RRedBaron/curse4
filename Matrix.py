import numpy as np
import matplotlib.pyplot as plt


class Matrix:
    def __init__(self, matrix):
        self.__order = len(matrix)
        self.__matrix = matrix

    # функція для визначення, чи є матриця симетричною
    def isMatrixSymmetric(self) -> bool:
        for i in range(1, len(self.__matrix)):
            for j in range(i):
                if self.__matrix[i][j] != self.__matrix[j][i]:
                    return False
        return True

    # функція для визначення виду матриці (діагональна/ні)
    def isMatrixDiagonal(self) -> bool:
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix)):
                if self.__matrix[i][j] != 0 and i != j:
                    return False
        return True

    def rotate_method(self, eps):

        def find_max(mat):
            max = 0
            for i in range(len(mat)):
                for j in range(len(mat)):
                    if abs(mat[i][j]) > abs(max):
                        max = mat[i][j]
            return max

        def find_max_coords(mat):
            max = 0
            coords = (0, 0)
            for i in range(len(mat)):
                for j in range(len(mat)):
                    if abs(mat[i][j]) > abs(max):
                        max = mat[i][j]
                        coords = (i, j)
            return coords

        A = self.__matrix
        (n, n) = np.shape(A)
        upperA = np.triu(A, 1)
        #Знаходження максимального елементу поза головною діагоналлю
        max_el = find_max(upperA)
        (k, m) = find_max_coords(upperA)
        # кут повороту
        if (A[k][k] - A[m][m]) == 0:
            phi = np.pi / 4
        else:
            phi = 1 / 2 * np.arctan(2 * A[k][m] / (A[k][k] - A[m][m]))

        E = np.eye(n)
        H = E
        H[k][k] = np.cos(phi)
        H[k][m] = -np.sin(phi)
        H[m][k] = np.sin(phi)
        H[m][m] = np.cos(phi)

        matH = []
        matH.append(H)
        matA = []
        matA.append(A)

        matA.append(np.dot(np.dot(np.linalg.inv(H), A), H))

        error = 100
        i = 1
        while error > eps:
            # Ітераційний процес
            A = matA[i]
            upperA = np.triu(A, 1)
            max_el = find_max(upperA)
            (k, m) = find_max_coords(upperA)
            if (A[k][k] - A[m][m]) == 0:
                phi = np.pi / 4
            else:
                phi = 1 / 2 * np.arctan(2 * A[k][m] / (A[k][k] - A[m][m]))
            E = np.eye(n)
            H = E
            H[k][k] = np.cos(phi)
            H[k][m] = -np.sin(phi)
            H[m][k] = np.sin(phi)
            H[m][m] = np.cos(phi)
            matH.append(H)
            if np.linalg.det(H) == 0:
                return
            matA.append(np.dot(np.dot(np.linalg.inv(H), A), H))
            error = abs(max_el)
            i = i + 1
        val = np.diag(matA[i])
        vecs = np.eye(n)
        for i in range(len(matH)):
            vecs = np.dot(vecs, matH[i])
        return val, vecs, i

    def danylevskyy_method(self):

        def move_el(mat, k, m): #функція для переставляння рядків і стовпців
            for i in range(len(mat)):
                temp = mat[k][i]
                mat[k][i] = mat[m][i]
                mat[m][i] = temp
            for i in range(len(mat)):
                temp = mat[i][k]
                mat[i][k] = mat[i][m]
                mat[i][m] = temp
            return mat

        def matrix_P(A): #знаходження матриці Фробеніуса
            counter = 1
            (n, n) = np.shape(A)
            B = np.eye(n)
            B_i = np.eye(n)
            try:
                for i in range(1, n):
                    if A[n - i][n - i - 1] == 0:
                        for l in reversed(range(n - i)):
                            counter += 1
                            if A[n - i][l] != 0:
                                A = move_el(A, n - i - 1, l)
                                break
                            if A[n - i][0] == 0:
                                n = n - i - 1
                    for j in range(n):
                        counter += 1
                        B_i[-(i + 1)][j] = -A[n - i][j] / A[n - i][n - i - 1]
                        if j == n - i - 1:
                            B_i[-(i + 1)][j] = 1 / A[n - i][n - i - 1]
                    A = np.linalg.inv(B_i).dot(A).dot(B_i)
                    B = B.dot(B_i)
                    B_i = np.eye(n)
                    n = len(A)
            except (ValueError, IndexError):
                return None, None, 0
            return A, B, counter

        A = np.array(self.__matrix)
        n = len(A)
        P, B, counter = matrix_P(A)
        if P is None and B is None:
            return False
        coefs = [1] + [-i for i in P[0]]
        eigenvalues = np.roots(coefs)
        eigenvectors = [B.dot(np.array([eig ** (n - i - 1) for i in range(n)]))
                        for eig in eigenvalues]
        return eigenvalues, eigenvectors, coefs, counter

    #метод для побудови графіку поліному
    def draw(self, poly):
        plt.close()
        roots = np.roots(poly)
        for i in roots:
            if i.imag:
                return False
        ur = np.poly1d(poly)
        x = np.linspace(np.amin(roots) - 2, np.amax(roots) + 2, 100)
        y = ur(x)
        plt.grid()
        plt.title("Графік полінома")
        plt.plot(x, y)
        plt.show()
        return True

    #функція для форматування результатів отриманих методом Данилевського
    @staticmethod
    def format_danilevskiy_results(input_text: tuple):
        text = ''
        for i in range(len(input_text[0])):
            text += "λ{} = {:.4f}".format(i+1, input_text[0][i]) + ' '
            if i % 2 == 1:
                text += '\n'
        text += '\n'
        for i in range(len(input_text[1])):
            text += f'x{i + 1} = '
            for k in range(len(input_text[1][i])):
                text += f'{round(input_text[1][i][k], 4)}\n     '
            text += '\n'
        return text

    #функція для форматування результатів отриманих методом обертань
    @staticmethod
    def format_rotation_results(input_text: tuple):
        text = ''
        for j in range(len(input_text[0])):
            text += f'λ{j + 1} = {round(input_text[0][j], 4)} '
            if j % 2 == 1:
                text += '\n'
        text += '\n'
        for j in range(len(input_text[1])):
            text += f'x{j + 1} = '
            for k in range(len(input_text[1][j])):
                text += f'{round(input_text[1][k][j], 4)}\n     '
            text += '\n'
        return text

    #спеціальна функція для візуалізації діагональної матриці
    @staticmethod
    def special_case_format(input_text: tuple):
        text = ''
        for i in range(len(input_text[0])):
            try:
                text += f'λ{i + 1} = {round(input_text[0][i], 4)} '
            except Exception as ex:
                text += f'λ{i + 1} = {input_text[i]} '
        text += '\n'
        for i in range(len(input_text[1])):
            text += f'x{i + 1} = '
            for k in range(len(input_text[1][i])):
                text += f'{round(input_text[1][k][i], 4)}\n     '
            text += '\n'
        return text
