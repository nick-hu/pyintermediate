#!/usr/bin/env python

import sys
import socket

from fltk import *


class ChessWin(Fl_Window):
    def __init__(self, player):
        text = "Chess: " + player
        super(self.__class__, self).__init__(500, 300, text)
        self.color(FL_WHITE)
        self.begin()

        self.you = Fl_Browser(20, 20, 150, 100)
        self.opp = Fl_Browser(330, 20, 150, 100)
        self.move = Fl_Input(20, 150, 75, 30)
        self.move_but = Fl_Return_Button(20, 190, 75, 30, "Move")
        self.move_but.callback(self.send)
        self.timer = Fl_Output(330, 150, 150, 50)
        self.timer.color(fl_rgb_color(40, 180, 0))
        self.timer.textsize(24)

        self.end()
        self.show()

        self.time, self.moves = 120, 0
        mins, secs = str(self.time // 60), str(self.time % 60)
        if len(secs) == 1:
            secs = "0" + secs
        self.timer.value(" " * 6 + mins + ":" + secs)

        self.wait = False if player == "client" else True
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if player == "client":
            self.send_addr = (sys.argv[3], int(sys.argv[2]))
        else:
            self.send_addr = ()
            self.conn.bind(("0.0.0.0", int(sys.argv[2])))
        Fl.add_fd(self.conn.fileno(), self.recv)

    def send(self, wid):
        if self.wait:
            return

        self.conn.sendto(self.move.value(), self.send_addr)
        self.you.add(self.move.value())
        self.move.value("")

        self.moves, self.wait = self.moves + 1, True
        if self.moves == 5:
            self.timer.value("")
            self.timer.color(fl_rgb_color(150, 150, 150))

    def recv(self, fd):
        data, self.send_addr = self.conn.recvfrom(1024)

        self.opp.add(data)
        self.wait = False
        if (self.moves < 5) and (self.time > 0):
            self.countdown()

    def countdown(self):
        if self.wait:
            return

        self.time = self.time - 1
        mins, secs = str(self.time // 60), str(self.time % 60)
        if len(secs) == 1:
            secs = "0" + secs
        self.timer.value(" " * 6 + mins + ":" + secs)

        if self.time == 0:
            self.timer.color(fl_rgb_color(240, 60, 60))
            self.timer.redraw()
            fl_message("Timeout! You lose :(")
            return
        if (self.time == 30) and (self.moves < 5):
            self.timer.color(fl_rgb_color(240, 215, 0))
            self.timer.redraw()
        Fl.repeat_timeout(1.0, self.countdown)


def main():
    win = ChessWin(sys.argv[1])

    Fl.scheme("gtk+")
    Fl.run()

if __name__ == "__main__":
    main()
