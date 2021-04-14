import numpy as np
import main

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4

def return_board(board):

    return_board = []
    for i in range(36):
        if board[i]!=4:
            return_board.append(board[i])

    return return_board


def convert_state(observation):

    return sum([stone * (3 ** i) for i, stone in enumerate(observation)])



player_list = ["player", "random"]
othello = main.Othello(player_list[1], player_list[1])
black_win = 0
white_win = 0

for i in range(10000):
    othello.reset()
    winner = othello.game_loop(4, 4)
    while winner==-1:
        winner = othello.game_loop(4, 4)
    if winner==BLACK:
        black_win += 1
    elif winner==WHITE:
        white_win += 1

print(black_win, white_win)