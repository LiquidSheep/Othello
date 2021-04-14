

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4

class Board():

    def __init__(self):

        self.board = [BLANK if i in [j*10+k for j in range(1, 9) for k in range(1, 9)] else WALL for i in range(100)]

        self.put_stone(44, WHITE)
        self.put_stone(45, BLACK)
        self.put_stone(54, BLACK)
        self.put_stone(55, WHITE)

        self.flip_list = []

    def put_stone(self, place, state):

        self.board[place] = state

    def flip_stone(self, place, color):

        direction_list = [-11, -10, -9, -1, 1, 9, 10, 11]

        num = 0
        for direction in direction_list:
            num += self.check_line(place, color, direction)

        self.flip_list.append(place)
        self.flip_list.append(num)

        return num

    def check_line(self, place, color, direction):

        num = 0
        i = place + direction

        while self.board[i]==color%2+1:
            i += direction

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
                self.restore_put(color)
                if flip_stone>0:
                    self.put_stone(i, PLACEABLE)

    def delete_placeable(self):

        for i in range(100):
            if self.board[i]==PLACEABLE:
                self.put_stone(i, BLANK)

    def restore_put(self, color):

        num = self.flip_list.pop(-1)
        self.put_stone(self.flip_list.pop(-1), BLANK)
        for i in range(num):
            self.put_stone(self.flip_list.pop(-1), color%2+1)

    def print_board(self):
        
        for i in range(10):
            for j in range(10):
                print(self.board[i*10+j], end=" ")
            print()
        print()

