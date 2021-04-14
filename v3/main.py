import board
import statistic
import display

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4


class Othello():

    def __init__(self, player_black, player_white):

        self.player_black = player_black
        self.player_white = player_white

        self.board_class = board.Board()
        self.pass_num = 0
        self.turn = BLACK
        self.game_end = False

        #self.display = display.Display()

        while not self.game_end:
            self.game_loop()

        #self.display.root.mainloop()

    def game_loop(self):

        if not BLANK in self.board_class.board:
            self.end_game(self.board_class.board)
            return

        if not WHITE in self.board_class.board:
            self.end_game(self.board_class.board)
            return

        if not BLACK in self.board_class.board:
            self.end_game(self.board_class.board)
            return

        self.board_class.find_placeable(self.turn)
        placeable_list = [i for i, place in enumerate(self.board_class.board) if place==PLACEABLE]
        if len(placeable_list)==0:
            if self.pass_num==2:
                self.end_game(self.board_class.board) 
                return
            else:
                self.pass_num += 1
                self.end_turn()
            #self.display.root.after(100, self.game_loop)
            return

        if self.turn==BLACK:
            if self.player_black=="player":
                s = statistic.Player(placeable_list)
            elif self.player_black=="random":
                s = statistic.Random(placeable_list)
            elif self.player_black=="static":
                s = statistic.StaticEval(placeable_list)
            elif self.player_black[:-1]=="alphabeta":
                s = statistic.Alphabeta(self.board_class, self.turn, self.player_black[-1])
        else:
            if self.player_white=="player":
                s = statistic.Player(placeable_list)
            elif self.player_white=="random":
                s = statistic.Random(placeable_list)
            elif self.player_white=="static":
                s = statistic.StaticEval(placeable_list)
            elif self.player_white[:-1]=="alphabeta":
                s = statistic.Alphabeta(self.board_class, self.turn, self.player_white[-1])

        
        place = s.return_place()

        self.board_class.put_stone(place, self.turn)
        self.board_class.flip_stone(place, self.turn)
        self.end_turn()

        self.board_class.print_board()

        #self.display.display_board(self.board_class.board)
        #self.display.root.after(100, self.game_loop)

    def end_turn(self):

        self.board_class.delete_placeable()
        self.turn = self.turn % 2 + 1

    def end_game(self, board):

        self.game_end = True

        global black_win
        global white_win
        global even
        black_num = len([i for i, p in enumerate(board) if p==BLACK])
        white_num = len([i for i, p in enumerate(board) if p==WHITE])

        print("black:", black_num, " white:", white_num)
        print()

        if black_num>white_num:
            black_win += 1
        elif black_num<white_num:
            white_win += 1
        else:
            even += 1

player_list = ["player", "random", "static", "alphabeta6"]
try_num = 1

black_win = 0
white_win = 0
even = 0
for i in range(try_num):
    Othello(player_list[1], player_list[3])

print("black_win", black_win)
print("white_win", white_win)
print("even", even)