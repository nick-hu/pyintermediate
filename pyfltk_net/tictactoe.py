#!/usr/bin/env python

import socket
import sys
import cPickle

from fltk import *


class TicTacToe(Fl_Window):
    def __init__(self, letter):
        side = "X (Client)" if letter == "X" else "O (Server)"
        side = "Tic-Tac-Toe: " + side
        super(self.__class__, self).__init__(335, 335, side)
        self.color(FL_WHITE)
        self.begin()

        backbox = Fl_Box(15, 15, 305, 305)
        backbox.box(FL_FLAT_BOX)
        backbox.color(FL_BLACK)

        self.grid, self.let = [], letter
        for y in xrange(3):
            self.grid.append([])
            for x in xrange(3):
                cell = Fl_Button(x*105 + 10, y*105 + 10, 100, 100)
                cell.box(FL_FLAT_BOX)
                cell.color(FL_WHITE)
                cell.labelsize(64)
                cell.labelfont(FL_HELVETICA_BOLD)
                cell.labelcolor(fl_rgb_color(240, 60, 60))
                cell.shortcut(str((3-y)*3 - 2 + x))
                cell.callback(self.send, (x, y))
                self.grid[-1].append(cell)

        self.end()
        self.show()

        self.wait = False if letter == "X" else True
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if letter == "X":
            self.send_addr = (sys.argv[2], int(sys.argv[3]))
        else:
            self.send_addr = ()
            self.conn.bind(("0.0.0.0", int(sys.argv[2])))
        Fl.add_fd(self.conn.fileno(), self.recv)

        self.rcdpos = []
        for rc in xrange(3):  # Row/column positions
            self.rcdpos.append([(rc, n) for n in xrange(3)])
            self.rcdpos.append([(n, rc) for n in xrange(3)])
        self.rcdpos.append([(n, n) for n in xrange(3)])  # Diagonal positions
        self.rcdpos.append([(n, 2-n) for n in xrange(3)])

    def send(self, wid, pos):
        x, y = pos
        if self.grid[y][x].label() or self.wait:
            return

        if self.let == "O":
            wid.labelcolor(fl_rgb_color(45, 150, 255))
        wid.label(self.let)
        self.conn.sendto(cPickle.dumps((self.let, x, y)), self.send_addr)
        self.wait = True
        self.chkwin()

    def recv(self, fd):
        data, addr = self.conn.recvfrom(1024)
        let, x, y = cPickle.loads(data)
        self.send_addr = addr

        if let == "O":
            self.grid[y][x].labelcolor(fl_rgb_color(45, 150, 255))
        self.grid[y][x].label(let)
        self.wait = False
        self.chkwin()

    def chkwin(self):
        state, winner = [[c.label() for c in row] for row in self.grid], ""
        for pos in self.rcdpos:
            case = [state[y][x] for x, y in pos]
            for let in ("X", "O"):
                if case.count(let) == 3:
                    winner = let

        if winner:
            if winner == self.let:
                fl_alert(self.let + " wins! :)")
            else:
                fl_alert(self.let + " loses! :(")
            self.wait = True  # Disable grid
        if not winner and all(l for row in state for l in row):
            fl_alert("Tie! :|")
            self.wait = True


def main():
    win = TicTacToe(sys.argv[1])  # X: client, O: server

    Fl.scheme("gtk+")
    Fl.run()

if __name__ == "__main__":
    main()
