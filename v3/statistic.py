import random


BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4

class StaticEval():

    def __init__(self, placeable_list):

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
        for p in placeable_list:
            if eval_list[p]>max_value:
                max_value = eval_list[p]
                self.place = p
            elif eval_list[p]==max_value:
                if random.getrandbits(1):
                    max_value = eval_list[p]
                    self.place = p

    def return_place(self):

        return self.place

class Random():

    def __init__(self, placeable_list):

        self.place = random.choice(placeable_list)

    def return_place(self):

        return self.place

class Player():

    def __init__(self, placeable_list):

        self.place = int(input("Enter place(11-88)"))

    def return_place(self):

        return self.place

class Alphabeta():

    def __init__(self, board_class, turn, depth):

        self.board_class = board_class
        self.turn = turn
        self.depth = int(depth)

    def eval(self, board, turn):

        self.board_class.find_placeable(turn)
        placeable_list = [place for place in board if place==PLACEABLE]
        self.board_class.delete_placeable()

        return len(placeable_list)

    def search(self, depth, alpha, beta, turn):

        if depth==0:
            return self.eval(self.board_class.board, turn)

        self.board_class.find_placeable(turn)
        placeable_list = [i for i, place in enumerate(self.board_class.board)if place==PLACEABLE]
        self.board_class.delete_placeable()

        if len(placeable_list)==0:
            if not BLANK in self.board_class.board:
                if len([place for place in self.board_class.board if place==self.turn])<\
                    len([place for place in self.board_class.board if place==self.turn%2+1]):
                    return 10000
                elif len([place for place in self.board_class.board if place==self.turn])<\
                    len([place for place in self.board_class.board if place==self.turn%2+1]):
                    return -10000
                else:
                    return 0
            else:
                turn = turn % 2 + 1

        for placeable in placeable_list:
            self.board_class.put_stone(placeable, turn)
            self.board_class.flip_stone(placeable, turn)
            value = self.search(depth-1, -beta, -alpha, turn%2+1)
            self.board_class.restore_put(turn)

            if turn==self.turn and value>=beta:
                return beta
            
            alpha = max(alpha, value)

        return alpha

    def return_place(self):

        self.board_class.find_placeable(self.turn)
        placeable_list = [i for i, place in enumerate(self.board_class.board) if place==PLACEABLE]
        self.board_class.delete_placeable()


        best_value = -10000
        best_place = -1
        
        for placeable in placeable_list:
            self.board_class.put_stone(placeable, self.turn)
            self.board_class.flip_stone(placeable, self.turn)
            value = self.search(self.depth-1, -10000, 10000, self.turn%2+1)
            self.board_class.restore_put(self.turn)

            if value>best_value:
                best_place = placeable

        return best_place