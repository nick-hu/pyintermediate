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

        self.send_addr, self.send_port = sys.argv[1:3]
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.fd = self.conn.fileno()
        Fl.add_fd(self.fd, self.recv)

    def recv(self, fd):
        data, addr = self.conn.recvfrom(1024)
        astr = "[" + addr[0] + ":" + str(addr[1]) + "] "
        self.disp.add(astr + data)

    def send(self, wid):
        addr = (self.send_addr, int(self.send_port))
        self.disp.add("[SELF] " + self.inp.value())
        self.conn.sendto(self.inp.value(), addr)
        self.inp.value("")


def main():
    win = Chat()

    Fl.scheme("gtk+")
    win.show()
    Fl.run()

if __name__ == "__main__":
    main()
