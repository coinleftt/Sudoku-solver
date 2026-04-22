# EDIT THE FILE WITH YOUR SOLUTION
import sys
from collections import defaultdict

class SudokuError(Exception):
    pass

class Sudoku(str):
    def __init__(self, filename) -> None:
        try:
            self.stri = r"""\documentclass[10pt]{article}
\usepackage[left=0pt,right=0pt]{geometry}
\usepackage{tikz}
\usetikzlibrary{positioning}
\usepackage{cancel}
\pagestyle{empty}

\newcommand{\N}[5]{\tikz{\node[label=above left:{\tiny #1},
                               label=above right:{\tiny #2},
                               label=below left:{\tiny #3},
                               label=below right:{\tiny #4}]{#5};}}

\begin{document}

\tikzset{every node/.style={minimum size=.5cm}}

\begin{center}
\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline
"""
            self.stri2 = r"""\hline
\end{tabular}
\end{center}

\end{document}
"""
            self.filename = filename
            board = []
            file = open(self.filename, "r").readlines()

            for i in file:
                if i.strip() == '':
                    continue

                subgrid = []

                if " " in i.strip():
                    nums = i.strip().split(" ")
                else:
                    nums = list(i.strip())

                while '' in nums:
                    nums.remove('')

                for j in range(len(nums)):
                    if nums[j] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        raise SudokuError                    
                    else:
                        subgrid.append(int(nums[j]))

                if len(subgrid) != 9:
                    raise SudokuError
                
                board.append(subgrid)

            if len(board) != 9:
                raise SudokuError

            self.board = board
            return None
        
        except SudokuError:
            print("sudoku.SudokuError: Incorrect input")
            sys.exit()
        
    def find_empty_cell(board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)
                
        return None
                
    def is_valid(board):
        def has_duplicates(nums):
            seen = set()
            for num in nums:
                if num != 0:
                    if num in seen:
                        return True
                    seen.add(num)
            return False

        for row in board:
            if has_duplicates(row):
                return False

        for col in zip(*board):
            if has_duplicates(col):
                return False

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if has_duplicates(subgrid):
                    return False

        return True
    
    def is_move_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True
    
    def mark(board):
        for row in range(9):
            for col in range(9):
                nums = []
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if Sudoku.is_move_valid(board, row, col, num):
                            nums.append(num)

                    board[row][col] = nums
        return board

    def force(board):
        grid = []
        run = True

        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                num_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
                subgrid = [board[i][col: col + 3] for i in range(row, row + 3)]

                for subrow in subgrid:
                    for cell in subrow:
                        if type(cell) == list:
                            for num in cell:
                                num_dict[num] += 1
                
                for x, y in num_dict.items():
                    if y == 1 and run:
                        for subrow in range(len(subgrid)):
                            for cell in range(len(subgrid[subrow])):
                                if type(subgrid[subrow][cell]) == list and x in subgrid[subrow][cell]:
                                    subgrid[subrow][cell] = x
                                    run = False

                grid.append(subgrid)

        return grid

    def form(subgrid_values):
        sudoku_board = [[0] * 9 for _ in range(9)]

        for i in range(9):
            for j in range(9):
                subgrid_index = (i // 3) * 3 + j // 3
                subgrid_row = i % 3
                subgrid_col = j % 3
                sudoku_board[i][j] = subgrid_values[subgrid_index][subgrid_row][subgrid_col]

        return sudoku_board

    def undo(board):
        for row in range(9):
            for col in range(9):
                if type(board[row][col]) == list:
                    board[row][col] = 0
                    
        return board
    
    def write_file(board, filename, mode, stri, stri2):
        code = ""

        for i in range(9):
            code += f"% Line {i+1}\n"

            for j in range(9):
                if board[i][j] == 0:
                    code += r"\N{}{}{}{}{}"

                else:
                    code += r"\N{}{}{}{}{" + str(board[i][j]) + r"}"

                if (j+1) % 3 == 0:
                    code += " &"
                else:
                    code += " & "

                if (j + 1) % 3 == 0:
                    code += "\n"

            code = code[:-3] + r" \\ \hline"

            if (i+1) % 3 == 0:
                code += "\hline\n\n"

            else:
                code += "\n\n"

        code = stri + code[:-8] + stri2

        with open(filename + "_" + mode + ".tex", 'w') as file:
            file.write(code)

    def preassess(self):
        if not Sudoku.is_valid(self.board):
            print("There is clearly no solution.")
            sys.exit()

        else:
            print("There might be a solution.")

    def bare_tex_output(self):
        Sudoku.write_file(self.board, self.filename[:-4], "bare", self.stri, self.stri2)

    def forced_tex_output(self):
        for i in range(81):
            self.board = Sudoku.undo(Sudoku.form(Sudoku.force(Sudoku.mark(self.board))))
        Sudoku.write_file(self.board, self.filename[:-4], "forced", self.stri, self.stri2)

    def marked_tex_output(self):
        board = Sudoku.mark(self.board)

        filename = self.filename[:-4] + "_marked.tex"
        code = ""
        l_1 = [1, 2]
        l_2 = [3, 4]
        l_3 = [5, 6]
        l_4 = [7, 8, 9]
        l_rl = [l_1, l_2, l_3, l_4]

        for i in range(9):
            code += f"% Line {i+1}\n"

            for j in range(9):
                if type(board[i][j]) == list:
                    board_save = defaultdict(str)

                    for item in board[i][j]:
                        for row in range(4):
                            if item in l_rl[row]:
                                board_save[row] = board_save[row] + str(item) + ' '

                    for row in board_save:
                        if board_save[row].endswith(' '):
                            board_save[row] = board_save[row][:-1]

                    code += '\\N{' + f'{board_save[0]}' + '}{' + f'{board_save[1]}' + '}{' + f'{board_save[2]}' + '}{' + f'{board_save[3]}' + r'}{}'

                else:
                    code += r"\N{}{}{}{}{" + str(board[i][j]) + r"}"
                
                if (j+1) % 3 == 0:
                    code += " &"
                else:
                    code += " & "

                if (j+1) % 3 == 0:
                    code += "\n"

            code = code[:-3] + r" \\ \hline"

            if (i+1) % 3 == 0:
                code += "\hline\n\n"

            else:
                code += "\n\n"

        code = self.stri + code[:-8] + self.stri2

        with open(filename, 'w') as file:
            file.write(code)

    def worked_tex_output(self):
        pass

su = Sudoku("sudoku.txt")
su.preassess()
su.bare_tex_output()
su.forced_tex_output()
su.marked_tex_output()