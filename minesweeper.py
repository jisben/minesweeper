#!/usr/bin/env python

from enum import Enum
import random
import time

automate = False

class SquareType(Enum):
    BLANK = 0
    NUMBER = 1
    BOMB = 2

class Square:
    def __init__(self):
        self.reset()
    def reset(self):
        self.type = SquareType.BLANK
        self.number = 0
        self.visible = False
        self.marked = False
    def is_marked(self):
        return self.marked
    def is_visible(self):
        return self.visible or self.marked
    def is_number(self):
        return self.type == SquareType.NUMBER
    def is_blank(self):
        return self.type == SquareType.BLANK


class MineSweeper:
    def __init__(self, size):
        """ Create a new minesweeper game """
        self.array = [[Square() for x in xrange(size)] for x in xrange(size)]
        self.init_game()

    def get_game_size(self):
        return len(self.array)

    def init_game(self):
        """ Init or re-init a board """
        nrows = len(self.array)
        self.game_over = False
        self.squares_left = nrows * nrows
        self.bombs_left = 0
        # clear the board
        for i in xrange(nrows):
            for j in xrange(nrows):
                self.array[i][j].reset()
        # put N random bombs
        for i in xrange(nrows):
            rand_num = random.randrange(nrows*nrows)
            if self.array[rand_num / nrows][rand_num % nrows].type \
                != SquareType.BOMB:
                self.insert_bomb(rand_num / nrows, rand_num % nrows)
        self.squares_left -= self.bombs_left
        self.print_board()

    def increment_square(self, row, col):
        """ Add 1 to all squares surrounding a bomb """
        if not self.valid_square(row, col):
            return
        square = self.array[row][col]
        if square.type == SquareType.BLANK:
            square.type = SquareType.NUMBER
        square.number += 1

    def insert_bomb(self, row, col):
        """ Insert a bomb """
        self.array[row][col].type = SquareType.BOMB
        self.bombs_left += 1
        # top
        self.increment_square(row-1, col-1)
        self.increment_square(row-1, col)
        self.increment_square(row-1, col+1)
        # side
        self.increment_square(row, col-1)
        self.increment_square(row, col+1)
        # bot
        self.increment_square(row+1, col-1)
        self.increment_square(row+1, col)
        self.increment_square(row+1, col+1)

    def print_board(self):
        row_len = len(self.array)
        for i in xrange(row_len):
            # first row
            if i == 0:
                print "  | " + " | ".join([str(x) for x in xrange(row_len)]) + " |"
                print "--+" + (row_len*4-1) * "-" + "+"
            line = str(i) + " |"
            for itm in self.array[i]:
                if itm.marked is True:
                    line += " X |"
                elif itm.visible is False:
                    line += " - |"
                elif itm.type == SquareType.BLANK:
                    line += "   |"
                elif itm.type == SquareType.BOMB:
                    line += " * |"
                elif itm.type == SquareType.NUMBER:
                    line += " " + str(itm.number) + " |"
            print line
            # last row
            if i == row_len - 1:
                print "--+" + (row_len*4-1) * "-" + "+"
        print "bombs left: " + str(self.bombs_left)

    def valid_square(self, row, col):
        """ Check indices """
        if row < 0 or row >= len(self.array) or col < 0 or col >= len(self.array):
            return False
        else:
            return True

    def uncover_blanks(self, row, col):
        """ Uncover blanks at this location """
        checked = {}
        to_be_checked = []
        to_be_checked.append((row, col))
        while len(to_be_checked) > 0:
            sq_row, sq_col = to_be_checked.pop()
            if checked.has_key((sq_row, sq_col)):
                continue
            checked[(sq_row, sq_col)] = True
            if not self.valid_square(sq_row, sq_col):
                continue
            if self.array[sq_row][sq_col].visible is True:
                continue
            square = self.array[sq_row][sq_col]
            square.visible = True
            self.squares_left -= 1
            if square.type == SquareType.BLANK:
                start_row = sq_row-1
                start_col = sq_col-1
                end_row = sq_row+1
                end_col = sq_col+1
                for i in range(start_row, end_row+1):
                    for j in range(start_col, end_col+1):
                        if not checked.has_key((i, j)):
                            to_be_checked.append((i, j))

    def uncover_square(self, row, col):
        if not self.valid_square(row, col):
            print "Invalid square! Please try again"
            return
        if self.game_over or self.squares_left == 0:
            print "Sorry! Please start a new game"
        square = self.array[row][col]
        if square.visible:
            print "Already played!"
        elif square.marked:
            print "Square is marked!"
        elif square.type == SquareType.BOMB:
            self.game_over = True
            square.visible = True
            self.bombs_left -= 1
            self.print_board()
            print "KAABOOOOOOMMM!!!!! GAME OVER!"
            return
        elif square.type == SquareType.BLANK:
            self.uncover_blanks(row, col)
        else: # SquareType.NUMBER
            self.squares_left -= 1
            square.visible = True

        self.print_board()
        if self.squares_left == 0:
            print "WINNER WINNER CHICKEN DINNER!"
            self.game_over = True

    def mark_square(self, row, col):
        if not self.valid_square(row, col):
            print "Invalid square! Please try again"
            return
        if self.game_over or self.squares_left == 0:
            self.print_board()
            print "Sorry! Please start a new game"
            return
        if self.array[row][col].marked:
            self.array[row][col].marked = False
            self.bombs_left += 1
        else:
            self.array[row][col].marked = True
            self.bombs_left -= 1
        self.print_board()

    def process_input(self, solver, user_input):
        user_input = user_input.split(" ")
        if len(user_input) > 0:
            if user_input[0] == "mark":
                if len(user_input) < 3:
                    return
                try:
                    row = int(user_input[1])
                    col = int(user_input[2])
                except ValueError:
                    return
                self.mark_square(row, col)
                return
            elif user_input[0] == "uncover":
                if len(user_input) < 3:
                    return
                try:
                    row = int(user_input[1])
                    col = int(user_input[2])
                except ValueError:
                    return
                self.uncover_square(row, col)
                return
            elif user_input[0] == "hint":
                print "Solver says", solver.get_hint()
                return
            elif user_input[0] == "init":
                self.init_game()
                solver = MineSweeperSolver(self)
                return
        print "I don't understand"
        MineSweeper.help_msg()

    def play(self):
        solver = MineSweeperSolver(self)
        MineSweeper.help_msg()
        while True:
            if automate:
                user_input = solver.get_hint()
                print user_input
                self.process_input(solver, user_input)
                if self.game_over:
                    break
            else:
                print ""
                user_input = raw_input("Enter your command: ")
                self.process_input(solver, user_input)


    @staticmethod
    def help_msg():
        print "You can say:"
        print " 'uncover {row} {col}' to uncover that square"
        print " 'mark {row} {col}' to mark a bomb in that square"
        print " 'hint' to get a hint"
        print " 'init' to start a new game"


class MineSweeperSolver:
    def __init__(self, game):
        self.game = game

    def mark_safe(self, x, y, unsure, mined, safe):
        game_size = len(self.game.array)
        for row in range(x-1, x+2):
            if row < 0 or row >= game_size:
                continue
            for col in range(y-1, y+2):
                if col < 0 or col >= game_size:
                    continue
                elif row == x and col == y:
                    continue
                elif self.game.array[row][col].is_visible():
                    continue
                elif not mined.has_key((row, col)):
                    safe[(row, col)] = True

    def find_mines(self, x, y, count, unsure, mined, safe):
        game_size = len(self.game.array)
        potential = []
        for row in range(x-1, x+2):
            if row < 0 or row >= game_size:
                continue
            for col in range(y-1, y+2):
                if col < 0 or col >= game_size:
                    continue
                elif row == x and col == y:
                    continue
                elif self.game.array[row][col].is_marked() or \
                    mined.has_key((row, col)):
                    count -= 1
                    if unsure.has_key((row, col)):
                        del unsure[(row, col)]
                    if count == 0:
                        # we've covered all the mines. mark the rest safe
                        self.mark_safe(x, y, unsure, mined, safe)
                        return
                elif not self.game.array[row][col].is_visible():
                    potential.append((row, col))
        if len(potential) == count:
            # these are all mines
            for itm in potential:
                mined[itm] = True
                if unsure.has_key(itm):
                    del unsure[itm]
        for itm in potential:
            unsure[itm] = True

    def get_hint(self):
        squares_in_play = []
        # scan and try to mark the next likely bomb
        unsure = {}
        mined = {}
        safe = {}
        game_size = len(self.game.array)
        for row in xrange(game_size):
            for col in xrange(game_size):
                if not self.game.array[row][col].is_visible():
                    squares_in_play.append((row, col))
                if self.game.array[row][col].is_visible() and \
                    self.game.array[row][col].is_number():
                    count = self.game.array[row][col].number
                    self.find_mines(row, col, count, unsure, mined, safe)

        for itm in mined.keys():
            # just one
            del mined[itm]
            return "mark " + str(itm[0]) + " " + str(itm[1])

        for itm in safe.keys():
            # just one
            del safe[itm]
            return "uncover " + str(itm[0]) + " " + str(itm[1])

        if len(squares_in_play) == 0 or self.game.game_over:
            return "Game Over!"

        viable_plays = [x for x in squares_in_play if\
            not unsure.has_key(x) and not mined.has_key(x)]
        if len(viable_plays) > 0:
            rand_num = random.randrange(len(viable_plays))
            return "uncover " + str(viable_plays[rand_num][0]) + " " +\
                str(viable_plays[rand_num][1])
        else:
            # Pure guess
            rand_num = random.randrange(len(squares_in_play))
            print "I have to guess... :-("
            return "uncover " + str(squares_in_play[rand_num][0]) + " " +\
                str(squares_in_play[rand_num][1])


def main():
    game = MineSweeper(9)
    game.play()




if __name__ == "__main__":
    main()
