import tkinter as tk
import random
import copy
import time

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

class Board():

    def __init__(self):

        self.board = [BLANK if i in [j*10+k for j in range(1, 9) for k in range(1, 9)] else WALL for i in range(100)]

        self.put_stone(44, WHITE)
        self.put_stone(45, BLACK)
        self.put_stone(54, BLACK)
        self.put_stone(55, WHITE)

    def put_stone(self, place, state):

        self.board[place] = state

    def flip_stone(self, place, color):

        direction_list = [-11, -10, -9, -1, 1, 9, 10, 11]
        self.flip_list = []

        num = 0
        for direction in direction_list:
            num += self.check_line(place, color, direction)

        if num>0:
            self.flip_list.append(place)

        return num

    def check_line(self, place, color, direction):

        num = 0
        i = place + direction

        while self.board[i]==color%2+1:
            if i+direction>=0 and i+direction<100:
                i += direction
            else:
                break

        if self.board[i]!=color:
            return 0

        i -= direction
        while place!=i:
            self.put_stone(i, color)
            self.flip_list.append(i)
            i -= direction
            num += 1

        return num

    def find_placeable(self, color):

        for i in range(100):
            if self.board[i]==BLANK:
                flip_stone = self.flip_stone(i, color)
                self.restore_flip(color)
                if flip_stone!=0:
                    self.put_stone(i, PLACEABLE)

    def restore_flip(self, color):

        for place in self.flip_list[:-1]:
            self.put_stone(place, color%2+1)

    def delete_placeable(self):

        for i in range(100):
            if self.board[i]==PLACEABLE:
                self.put_stone(i, BLANK)

    def restore_put(self, color):

        self.restore_flip(color)
        self.put_stone(self.flip_list[-1], BLANK)

class Othello():

    def __init__(self, player_black, player_white):
        
        self.turn = BLACK
        self.pass_num = 0
        self.player_black = player_black
        self.player_white = player_white

        self.board_class = Board()
        self.display = Display()

        self.game_loop()

        self.display.root.mainloop()

    def game_loop(self):

        if not BLANK in self.board_class.board:
            self.game_end(self.board_class.board)
            return

        if not WHITE in self.board_class.board:
            self.game_end(self.board_class.board)
            return

        if not BLACK in self.board_class.board:
            self.game_end(self.board_class.board)
            return

        self.board_class.find_placeable(self.turn)
        self.placeable_list = [i for i, place in enumerate(self.board_class.board) if place==PLACEABLE]
        if len(self.placeable_list)==0:
            if self.pass_num==2:
                self.game_end(self.board_class.board)  
                return
            else:
                self.pass_num += 1
                self.end_turn()

            self.display.root.after(wait, self.game_loop)
            return

        if self.turn==BLACK:
            if self.player_black=="player":
                self.player()
            elif self.player_black=="random":
                self.random()
            elif self.player_black=="static":
                self.static_eval()
            elif self.player_black[:-1]=="minimax":
                self.decision_tree(self.player_black)
            elif self.player_black[:-1]=="alphabeta":
                self.decision_tree(self.player_black)
        else:
            if self.player_white=="player":
                self.player()
            elif self.player_white=="random":
                self.random()
            elif self.player_white=="static":
                self.static_eval()
            elif self.player_white[:-1]=="minimax":
                self.decision_tree(self.player_white)
            elif self.player_white[:-1]=="alphabeta":
                self.decision_tree(self.player_white)

        self.display.root.after(wait, self.game_loop)

    def game_end(self, board):

        global black_win
        global white_win
        global even
        black_num = len([i for i, p in enumerate(board) if p==BLACK])
        white_num = len([i for i, p in enumerate(board) if p==WHITE])
        """print("black:", black_num)
        print("white:", white_num)
        print()"""

        if black_num>white_num:
            black_win += 1
        elif black_num<white_num:
            white_win += 1
        else:
            even += 1
        self.display.root.destroy()

    def random(self):

        place = random.choice(self.placeable_list)

        self.board_class.put_stone(place, self.turn)
        self.board_class.flip_stone(place, self.turn)
        self.end_turn()
        
        self.display.display_board(self.board_class.board)

    def static_eval(self):

        eval_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 100, -40, 20, 5, 5, 20, -40, 100, 0,
                     0, -40, -80, -1, -1, -1, -1, -80, -40, 0,
                     0, 20, -1, 5, 1, 1, 5, -1, 20, 0,
                     0, 5, -1, 1, 0, 0, 1, -1, 5, 0,
                     0, 5, -1, 1, 0, 0, 1, -1, 5, 0,
                     0, 20, -1, 5, 1, 1, 5, -1, 20, 0,
                     0, -40, -80, -1, -1, -1, -1, -80, -40, 0,
                     0, 100, -40, 20, 5, 5, 20, -40, 100, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        max_value = -100
        for p in self.placeable_list:
            if eval_list[p]>max_value:
                max_value = eval_list[p]
                place = p

        self.board_class.put_stone(place, self.turn)
        self.board_class.flip_stone(place, self.turn)
        self.end_turn()
        
        self.display.display_board(self.board_class.board)

    def decision_tree(self, tactics):

        decision_tree_class = Decision_tree(self.turn)
        
        if tactics[:-1]=="minimax":
            place = decision_tree_class.decide_place_minimax(self.board_class, self.turn, int(tactics[-1]))
        elif tactics[:-1]=="alphabeta":
            place = decision_tree_class.decide_place_alphabeta(self.board_class, self.turn, int(tactics[-1]))

        self.board_class.put_stone(place, self.turn)
        self.board_class.flip_stone(place, self.turn)
        self.end_turn()

        self.display.display_board(self.board_class.board)

    def player(self):

        self.display.root.bind("<1>", self.click_event)
        self.display.display_board(self.board_class.board)

    def click_event(self, event):

        if event.x>=20 and event.x<=180:
            if event.y>=20 and event.y<=180:
                x = int(event.x/20)
                y = int(event.y/20)

                if self.board_class.board[y*10+x]==PLACEABLE:
                    self.board_class.put_stone(y*10+x, self.turn)
                    self.board_class.flip_stone(y*10+x, self.turn)
                    self.end_turn()

        self.display.display_board(self.board_class.board)

    def end_turn(self):

        self.display.root.unbind("<1>")
        self.board_class.delete_placeable()
        self.turn = self.turn % 2 + 1

class Decision_tree():

    def __init__(self, turn):

        self.turn = turn

    def decide_place_minimax(self, board_class, turn, depth):

        self.start = time.time()

        board_class_copy = copy.deepcopy(board_class)

        board_class_copy.find_placeable(turn)
        placeable_list = [i for i, place in enumerate(board_class_copy.board) if place==PLACEABLE]
        board_class_copy.delete_placeable()

        max_value = -10000
        best_place = -1
        for place in placeable_list:
            board_class_copy.put_stone(place, turn)
            board_class_copy.flip_stone(place, turn)
            value = self.minimax(board_class_copy, turn%2+1, depth-1)
            board_class_copy.restore_put(turn)

            if value>max_value:
                best_place = place

        return best_place

    def minimax(self, board_class, turn, depth):

        board_class_copy = copy.deepcopy(board_class)

        board_class_copy.find_placeable(turn)
        if not BLANK in board_class_copy.board:
            board_class_copy.delete_placeable()
            return self.eval_1(board_class_copy.board, turn)
        elif not PLACEABLE in board_class_copy.board:
            turn = turn % 2 + 1
            return self.eval_1(board_class_copy.board, turn)
        elif depth==0:
            board_class_copy.delete_placeable()
            return self.eval_1(board_class_copy.board, turn)

        placeable_list = [i for i, place in enumerate(board_class_copy.board) if place==PLACEABLE]
        board_class_copy.delete_placeable()

        max_value = -10000
        for place in placeable_list:
            board_class_copy.put_stone(place, turn)
            board_class_copy.flip_stone(place, turn)
            value = self.minimax(board_class_copy, turn%2+1, depth-1)
            board_class_copy.restore_put(turn)

            if turn==self.turn and value>max_value:
                max_value = value
            if turn==self.turn%2+1 and -value>max_value:
                max_value = -value

        return max_value

    def decide_place_alphabeta(self, board_class, turn, depth):

        self.start = time.time()

        board_class_copy = copy.deepcopy(board_class)

        board_class_copy.find_placeable(turn)
        placeable_list = [i for i, place in enumerate(board_class_copy.board) if place==PLACEABLE]
        board_class_copy.delete_placeable()

        max_value = -10000
        alpha = -10000
        beta = 10000
        best_place = -1
        for place in placeable_list:
            board_class_copy.put_stone(place, turn)
            board_class_copy.flip_stone(place, turn)
            value = self.alphabeta(board_class_copy, turn%2+1, depth-1, alpha, beta)
            board_class_copy.restore_put(turn)

            if value>max_value:
                best_place = place

        return best_place

    def alphabeta(self, board_class, turn, depth, alpha, beta):

        board_class_copy = copy.deepcopy(board_class)

        board_class_copy.find_placeable(turn)
        if not BLANK in board_class_copy.board:
            board_class_copy.delete_placeable()
            return self.eval_2(board_class_copy.board, turn)
        elif not PLACEABLE in board_class_copy.board:
            turn = turn % 2 + 1
            return self.eval_2(board_class_copy.board, turn)
        elif depth==0:
            board_class_copy.delete_placeable()
            return self.eval_2(board_class_copy.board, turn)

        placeable_list = [i for i, place in enumerate(board_class_copy.board) if place==PLACEABLE]
        board_class_copy.delete_placeable()

        for place in placeable_list:
            board_class_copy.put_stone(place, turn)
            board_class_copy.flip_stone(place, turn)
            value = self.alphabeta(board_class_copy, turn%2+1, depth-1, alpha, beta)
            board_class_copy.restore_put(turn)

            if turn==self.turn and value>alpha:
                alpha = value
                if alpha>=beta:
                    return beta
            if turn==self.turn%2+1 and value<beta:
                beta = value
                if beta<=alpha:
                    return alpha

        if turn==self.turn:
            return alpha
        if turn==self.turn%2+1:
            return beta

    def eval_1(self, board, turn):

        self.eval_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 100, -40, 20, 5, 5, 20, -40, 100, 0,
                     0, -40, -80, -1, -1, -1, -1, -80, -40, 0,
                     0, 20, -1, 5, 1, 1, 5, -1, 20, 0,
                     0, 5, -1, 1, 0, 0, 1, -1, 5, 0,
                     0, 5, -1, 1, 0, 0, 1, -1, 5, 0,
                     0, 20, -1, 5, 1, 1, 5, -1, 20, 0,
                     0, -40, -80, -1, -1, -1, -1, -80, -40, 0,
                     0, 100, -40, 20, 5, 5, 20, -40, 100, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        value = 0
        for i in range(100):
            if board[i]==turn:
                value += self.eval_list[i]
            elif board[i]==turn%2+1:
                value -= self.eval_list[i]

        return value

    def eval_2(self, board, turn):

        eval_value = self.eval_1(board, turn)
        placeable_value = self.eval_placeable(board)
        definite_value = self.eval_definite(board, turn)

        return definite_value*5

    def eval_definite(self, board, turn):

        corner_list = [11, 18, 81, 88]
        corner_direction_list = [[1, 10], [-1, 10], [1, -10], [-1, -10]]

        value = 0
        for i, corner in enumerate(corner_list):
            if board[corner]==turn:
                value += 1
                for direction in corner_direction_list[i]:
                    place = corner+direction
                    while board[place]==turn:
                        value += 1
                        place += direction
            if board[corner]==turn%2+1:
                for direction in corner_direction_list[i]:
                    place = corner+direction
                    while board[place]==turn:
                        value += 1
                        place += direction

        return value

    def eval_placeable(self, board):

        return len([place for place in board if place==PLACEABLE])

wait = 100
player_list = ["player", "random", "static", "minimax3", "alphabeta4"]

try_num = 100


black_win = 0
white_win = 0
even = 0
Othello(player_list[0], player_list[3])
print(black_win, white_win)