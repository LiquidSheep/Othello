import sys
import tkinter as tk

root = tk.Tk()
root.title("othello")
root.geometry("200x200")

canvas = tk.Canvas(root, width = 200, height = 200)
canvas.place(x=0, y=0)

def create_board():

    canvas.create_rectangle(20, 20, 180, 180, fill="green", outline="")
    for i in range(9):
        canvas.create_line(20, 20+20*i, 180, 20+20*i, fill="black", width=1)
        canvas.create_line(20+20*i, 20, 20+20*i, 180, fill="black", width=1)
    for i in range(2):
        for j in range(2):
            canvas.create_oval(59+80*i, 59+80*j, 61+80*i, 61+80*j, fill="black", width=2)


def put(putx, puty, c):

    canvas.create_rectangle(23+putx*20, 23+puty*20, 37+putx*20, 37+puty*20, fill="black" if c==1 else "white", outline="")
    replace_data(puty*8+putx, str(c))


def replace_data(i, state):

    global data
    temp = ""
    for j in range(65):
        if j==i:
            temp += state
        else:
            temp += data[j]
    data = temp


def upload_data():

    global data
    with open("./data.txt", "w", encoding="utf-8") as f:
        f.write(data)


def download_data():

    global data
    with open("./data.txt", "r", encoding="utf-8") as f:
        data = f.read()


def init_data():

    global data
    for i in range(65):
        data += "a"


def init(c):

    global my_color
    my_color = c
    init_data()
    create_board()
    put(3, 4, 1)
    put(3, 3, 2)
    put(4, 4, 2)
    put(4, 3, 1)
    upload_data()

data = ""
my_color = 0
init(1)

root.mainloop()