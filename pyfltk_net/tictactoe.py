#!/usr/bin/env python

import socket
import sys
import cPickle

from fltk import *


class TicTacToe(Fl_Window):
    def __init__(self, letter):
        super(self.__class__, self).__init__(335, 400, "Tic-Tac-Toe")
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

    def send(self, wid, pos):
        x, y = pos
        if self.grid[y][x].label() or self.wait:
            return
        wid.label(self.let)
        self.conn.sendto(cPickle.dumps((self.let, x, y)), self.send_addr)
        self.wait = True
        self.chkwin()

    def recv(self, fd):
        data, addr = self.conn.recvfrom(1024)
        let, x, y = cPickle.loads(data)
        if not self.send_addr:
            self.send_addr = addr

        self.grid[y][x].label(let)
        self.wait = False
        self.chkwin()

    def chkwin(self):
        x_pos, o_pos = [(-1, -1)], [(-1, -1)]  # -1 is a placeholder value
        for y in xrange(3):
            for x in xrange(3):
                if self.grid[y][x].label() == "X":
                    x_pos.append((y, x))
                if self.grid[y][x].label() == "O":
                    o_pos.append((y, x))
        print x_pos, o_pos
        x_pos, o_pos = zip(*x_pos), zip(*o_pos)
        print x_pos, o_pos

        diag_win_x, diag_win_o = True, True
        for rc in xrange(3):
            for xy in xrange(2):
                if x_pos[xy].count(rc) == 3:
                    print "Win X"
                if o_pos[xy].count(rc) == 3:
                    print "Win O"
                if rc not in x_pos[xy]:
                    diag_win_x = False
                if rc not in o_pos[xy]:
                    diag_win_o = False

        if diag_win_o:
            print "Win O diag"



def main():
    win = TicTacToe(sys.argv[1])  # X: client, O: server

    Fl.scheme("gtk+")
    Fl.run()

if __name__ == "__main__":
    main()
