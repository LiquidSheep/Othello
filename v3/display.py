import tkinter as tk

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4

class Display():

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Othello")
        self.root.geometry("200x200")
        self.canvas = tk.Canvas(self.root, width=200, height=200)

    def display_board(self, board):

        self.canvas.create_rectangle(0, 0, 200, 200, fill="white")
        self.canvas.create_rectangle(20, 20, 180, 180, fill="green", outline="")
        for i in range(9):
            self.canvas.create_line(20, 20+20*i, 180, 20+20*i, fill="black", width=1)
            self.canvas.create_line(20+20*i, 20, 20+20*i, 180, fill="black", width=1)
        for i in range(2):
            for j in range(2):
                self.canvas.create_oval(59+80*i, 59+80*j, 61+80*i, 61+80*j, fill="black", width=2)

        for i in range(100):
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
            x = i % 10
            y = i // 10
            self.canvas.create_rectangle(3+x*20, 3+y*20, 17+x*20, 17+y*20, fill=color, outline="")

        self.canvas.place(x=0, y=0)