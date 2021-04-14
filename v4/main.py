import board
import statistic
import display

BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4


class Othello:

    def __init__(self, player_black, player_white):

        self.player_black = player_black
        self.player_white = player_white

    def reset(self):

        self.board_class = board.Board()
        self.pass_num = 0
        self.turn = BLACK
        self.game_end = False

    def game_loop(self, place):

        if not BLANK in self.board_class.board:
            return self.end_game()

        if not WHITE in self.board_class.board:
            return self.end_game()

        if not BLACK in self.board_class.board:
            return self.end_game()

        self.board_class.find_placeable(self.turn)
        placeable_list = [i for i, place in enumerate(self.board_class.board) if place==PLACEABLE]
        self.board_class.delete_placeable()
        if len(placeable_list)==0:
            if self.pass_num==2:
                return self.end_game()
            else:
                self.pass_num += 1
                self.end_turn()
                return -1
        else:
            if self.turn==BLACK:
                if place==4:
                    if self.player_black=="player":
                        s = statistic.Player(placeable_list)
                    elif self.player_black=="random":
                        s = statistic.Random(placeable_list)
                    place = s.return_place()
            elif self.turn==WHITE:
                if place==4:
                    if self.player_white=="player":
                        s = statistic.Player(placeable_list)
                    elif self.player_white=="random":
                        s = statistic.Random(placeable_list)
                    place = s.return_place()

            self.board_class.put_stone(place, self.turn)
            self.board_class.flip_stone(place, self.turn)
            self.end_turn()

        return -1

    def end_turn(self):

        self.board_class.delete_placeable()
        self.turn = self.turn % 2 + 1

    def end_game(self):

        self.game_end = True

        black_num = len([i for i, p in enumerate(self.board_class.board) if p==BLACK])
        white_num = len([i for i, p in enumerate(self.board_class.board) if p==WHITE])

        if black_num>white_num:
            return BLACK
        elif black_num<white_num:
            return WHITE
        else:
            return BLANK