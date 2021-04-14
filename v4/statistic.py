import random


BLANK = 0
BLACK = 1
WHITE = 2
PLACEABLE = 3
WALL = 4

class Random:

    def __init__(self, placeable_list):

        self.place = random.choice(placeable_list)

    def return_place(self):

        return self.place

class Player:

    def __init__(self, placeable_list):

        self.place = int(input("Enter place(7-28)"))

    def return_place(self):

        return self.place