#!/usr/bin/env python

import socket
import sys

from fltk import *


class TicTacToe(Fl_Window):
    def __init__(self, letter):
        super(self.__class__, self).__init__(335, 400, "Tic-Tac-Toe")
        self.color(FL_WHITE)
        self.begin()

        backbox = Fl_Box(15, 15, 305, 305)
        backbox.box(FL_FLAT_BOX)
        backbox.color(FL_BLACK)
        for y in xrange(3):
            for x in xrange(3):
                cell = Fl_Button(x*105 + 10, y*105 + 10, 100, 100)
                cell.box(FL_FLAT_BOX)
                cell.color(FL_WHITE)
                cell.shortcut(str((3-y)*3 - 2 + x))
                cell.labelsize(64)
                cell.labelfont(FL_HELVETICA_BOLD)
                cell.callback(self.send, 3*y + x)

        self.state, self.let, self.wait = [""] * 9, letter, False

        self.end()
        self.show()

    def send(self, wid, pos):
        if self.state[pos] or self.wait:
            return
        wid.label(self.let)
        self.wait = True


def main():
    win = TicTacToe("X")

    Fl.scheme("gtk+")
    Fl.run()

if __name__ == "__main__":
    main()
