import tkinter as tk

def callback(i):
    def button_pushed():
        b[i].config(bg="black")
    return i

root = tk.Tk()
root.geometry("600x600")
root.title("tic tac toe")
frame = tk.Frame(root)
frame.place(x=100, y=100)

b = []
for row in range(8):
    for column in range(8):
        b.append(tk.Button(root, width=4, height=2))
        b[row*8+column].grid(row=row, column=column)
        b[row*8+column].config(command=callback(row*8+column))


root.mainloop()