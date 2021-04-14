import random

PUTTABLE = 3

def random_choice(board):

    random_range = []
    for i in range(100):
        if board[i]==PUTTABLE:
            random_range.append(i)
    
    return random.choice(random_range)

def static_eval1(board):

    eval_list_1 =  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 30, -12, 0, -1, -1, 0, -12, 30, 0],
                    [0, -12, -15, -3, -3, -3, -3, -15, -12, 0],
                    [0, 0, -3, 0, -1, -1, 0, -3, 0, 0],
                    [0, -1, -3, -1, -1, -1, -1, -3, -1, 0],
                    [0, -1, -3, -1, -1, -1, -1, -3, -1, 0],
                    [0, 0, -3, 0, -1, -1, 0, -3, 0, 0],
                    [0, -12, -15, -3, -3, -3, -3, -15, -12, 0],
                    [0, 30, -12, 0, -1, -1, 0, -12, 30, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    max_value = -100

    for i in range(1, 9):
        for j in range(1, 9):
            if board[i*10+j]==PUTTABLE:
                if board[i*10+j]*eval_list_1[i][j]>max_value:
                    max_value = board[i*10+j]*eval_list_1[i][j]
                    place = i*10+j

    if max_value==-100:
        return -1

    return place