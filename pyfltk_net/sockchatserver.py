#!/usr/bin/env python

import socket
import sys

from fltk import *


class Chat(Fl_Window):
    def __init__(self):
        super(self.__class__, self).__init__(500, 500, "Socket chat")
        self.color(FL_WHITE)
        self.begin()

        self.disp = Fl_Multi_Browser(10, 10, 480, 440)
        self.disp.color(FL_WHITE, fl_rgb_color(200, 200, 200))
        self.inp = Fl_Input(10, 460, 400, 30)
        send_but = Fl_Return_Button(420, 460, 70, 30, "Send")
        send_but.color(fl_rgb_color(50, 160, 255), fl_rgb_color(50, 160, 255))
        send_but.callback(self.send)

        self.end()

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn.bind(("0.0.0.0", int(sys.argv[1])))
        self.fd = self.conn.fileno()
        Fl.add_fd(self.fd, self.recv)

    def recv(self, fd):
        data, self.addr = self.conn.recvfrom(1024)
        astr = "[" + self.addr[0] + ":" + str(self.addr[1]) + "] "
        self.disp.add(astr + data)

    def send(self, wid):
        self.disp.add("[SELF] " + self.inp.value())
        self.conn.sendto(self.inp.value(), self.addr)
        self.inp.value("")


def main():
    win = Chat()

    Fl.scheme("gtk+")
    win.show()
    Fl.run()

if __name__ == "__main__":
    main()
