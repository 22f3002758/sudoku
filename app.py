import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.cells = {}
        self.create_board()
        self.generate_puzzle()

    def create_board(self):
        # Create a main frame
        main_frame = tk.Frame(self.master, bd=3, relief=tk.RAISED)
        main_frame.pack(padx=10, pady=10)

        # Create 3x3 frames for each box
        box_frames = [[tk.Frame(main_frame, bd=1, relief=tk.RAISED) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                box_frames[i][j].grid(row=i, column=j, padx=(0, 1), pady=(0, 1))

        for i in range(9):
            for j in range(9):
                cell = tk.Entry(box_frames[i//3][j//3], width=3, font=('Arial', 18), justify='center')
                cell.grid(row=i%3, column=j%3, padx=(0, 1), pady=(0, 1))
                cell.bind('<FocusIn>', self.cell_selected)
                cell.bind('<Key>', self.key_pressed)
                self.cells[(i, j)] = cell

        # Add check button below the main frame
        check_button = tk.Button(self.master, text="Check Solution", command=self.check_solution, font=('Arial', 12))
        check_button.pack(pady=10)

    def generate_puzzle(self):
        # Simple puzzle generation (not guaranteed to be uniquely solvable)
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return random.sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = squares * 3 // 4
        for p in random.sample(range(squares), empties):
            board[p // side][p % side] = 0

        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(board[i][j]))
                    self.cells[(i, j)].config(state='readonly', disabledbackground='white', disabledforeground='black')

    def cell_selected(self, event):
        cell = event.widget
        cell.delete(0, tk.END)

    def key_pressed(self, event):
        cell = event.widget
        if event.char in '123456789':
            cell.delete(0, tk.END)
            cell.insert(0, event.char)
        elif event.keysym in ('BackSpace', 'Delete'):
            cell.delete(0, tk.END)

    def check_solution(self):
        for i in range(9):
            row = [int(self.cells[(i, j)].get() or 0) for j in range(9)]
            if len(set(row)) != 9 or 0 in row:
                messagebox.showinfo("Result", "Incorrect! Keep trying.")
                return

        for j in range(9):
            col = [int(self.cells[(i, j)].get() or 0) for i in range(9)]
            if len(set(col)) != 9 or 0 in col:
                messagebox.showinfo("Result", "Incorrect! Keep trying.")
                return

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [int(self.cells[(i, j)].get() or 0) 
                       for i in range(box_row, box_row + 3) 
                       for j in range(box_col, box_col + 3)]
                if len(set(box)) != 9 or 0 in box:
                    messagebox.showinfo("Result", "Incorrect! Keep trying.")
                    return

        messagebox.showinfo("Result", "Correct! Well done!")

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()