import tkinter as tk

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4

class Display:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Othello")
        self.root.geometry("200x200")
        self.canvas = tk.Canvas(self.root, width=200, height=200)

    def display_board(self, board):

        self.canvas.create_rectangle(0, 0, 200, 200, fill="white")
        self.canvas.create_rectangle(10, 10, 190, 190, fill="green", outline="")
        for i in range(9):
            self.canvas.create_line(30, 30+30*i, 190, 10+30*i, fill="black", width=1)
            self.canvas.create_line(10+30*i, 10, 10+30*i, 190, fill="black", width=1)

        for i in range(36):
            state = board[i]
            if state==BLANK:
                color = "green"
            elif state==BLACK:
                color = "black"
            elif state==WHITE:
                color = "white"
            elif state==PLACEABLE:
                color = "sky blue"
            else:
                color = "white"
            x = i % 6
            y = i // 6
            self.canvas.create_rectangle(13+x*30, 13+y*30, 37+x*30, 37+y*30, fill=color, outline="")

        self.canvas.place(x=0, y=0)