import random
import tkinter as tk
import ai
import time

wait_time = 100

black_win = 0
white_win = 0

board = []
pass_num = 0

BLANK = 0
BLACK = 1
WHITE = 2
PUTTABLE = 3
WALL = 4

turn = BLACK
player = BLACK

root = tk.Tk()
root.title("Othello")
root.geometry("200x200")

canvas = tk.Canvas(root, width=200, height=200)

def draw_board():

    canvas.create_rectangle(20, 20, 180, 180, fill="green", outline="")
    for i in range(9):
        canvas.create_line(20, 20+20*i, 180, 20+20*i, fill="black", width=1)
        canvas.create_line(20+20*i, 20, 20+20*i, 180, fill="black", width=1)
    for i in range(2):
        for j in range(2):
            canvas.create_oval(59+80*i, 59+80*j, 61+80*i, 61+80*j, fill="black", width=2)

def put_stone(place, s):

    if s==BLANK:
        color = "green"    
    elif s==WHITE:
        color = "white"
    elif s==BLACK:
        color = "black"
    elif s==PUTTABLE:
        color = "sky blue"

    board[place] = s
    x = place % 10
    y = place // 10
    canvas.create_rectangle(3+x*20, 3+y*20, 17+x*20, 17+y*20, fill=color, outline="")

def board_init():

    global board
    board = []
    for i in range(100):
        board.append(WALL)
    for i in range(1, 9):
        for j in range(1, 9):
            board[i*10+j] = BLANK
    put_stone(44, WHITE)
    put_stone(45, BLACK)
    put_stone(54, BLACK)
    put_stone(55, WHITE)

def player_turn(event):

    global turn

    if event.x>=20 and event.x<=180:
        if event.y>=20 and event.y<=180:
            x = int(event.x/20)
            y = int(event.y/20)
            put_stone(y*10+x, turn)
            flip_stone(y*10+x, turn, False)

def no_puttable_random(board):

    blank_list = []
    for i in range(100):
        if board[i]==BLANK:
            blank_list.append(i)
    
    return random.choice(blank_list)

def check_line(place, direction, color, puttable):

    num = 0
    i = place + direction

    while board[i]==(color%2+1):
        if i+direction>=0 and i+direction<100:
            i += direction
    
    if board[i]!=color:
        return 0

    i -= direction
    while place!=i:
        if puttable==False:
            put_stone(i, color)
        i -= direction
        num += 1

    if puttable and num!=0:
        put_stone(i, PUTTABLE)

    return num

def flip_stone(place, color, puttable):

    direction_list = [-11, -10, -9, -1, 1, 9, 10, 11]

    num = 0
    for direction in direction_list:
        num += check_line(place, direction, color, puttable)

    return num

def detect_puttbale(color):

    for i in range(100):
        if board[i]==BLANK:
            flip_stone(i, color, True)

def delete_puttable():

    for i in range(100):
        if board[i]==PUTTABLE:
            put_stone(i, BLANK)

def calc_point():

    point_black = 0
    point_white = 0

    for i in range(100):
        if board[i]==BLACK:
            point_black += 1
        elif board[i]==WHITE:
            point_white += 1

    global black_win
    global white_win
    if point_black>point_white:
        black_win += 1
    elif point_black<point_white:
        white_win += 1

    return [point_black, point_white]

def main():

    global turn
    global pass_num
    detect_puttbale(turn)
    if PUTTABLE in board:
        pass_num = 0
        if turn==BLACK:
            place = ai.static_eval1(board)
        else:
            place = ai.static_eval1(board)
        put_stone(place, turn)
        flip_stone(place, turn, False)
    else:
        if pass_num==2:
            place = no_puttable_random(board)
            put_stone(place, turn)
            flip_stone(place, turn, False)
        else:
            pass_num += 1
    delete_puttable()
    turn = turn % 2 + 1

    if not BLANK in board:
        loop()
    else:
        root.after(wait_time, main)

def init():

    global turn
    turn = BLACK
    draw_board()
    board_init()

def loop():

    global loop_num
    loop_num -= 1

    if loop_num>=0:
        init()
        root.after(wait_time, main)
    else:
        return

loop_num = 100
loop()
canvas.place(x=0, y=0)

root.mainloop()