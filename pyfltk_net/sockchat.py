#!/usr/bin/env python

import socket
import sys

from fltk import *

class Chat(Fl_Window):
    def __init__(self):
        self.addr = socket.gethostbyname(socket.gethostname())

        super(self.__class__, self).__init__(500, 500, "Socket chat")
        self.color(FL_WHITE)
        self.begin()

        but_labels = ["&Add chatter", "&Remove chatter"]
        but_colors = [(80, 190, 50), (215, 55, 10)]
        but_colors = map(lambda rgb: fl_rgb_color(*rgb), but_colors)

        for x in xrange(len(but_labels)):
            but = Fl_Button(10 + 130 * x, 10, 120, 30, but_labels[x])
            but.color(but_colors[x], but_colors[x])
            but.callback(self.but_cb)

        self.disp = Fl_Hold_Browser(10, 50, 480, 400)
        self.inp = Fl_Input(10, 460, 400, 30)
        send_but = Fl_Return_Button(420, 460, 70, 30, "Send")
        send_but.color(fl_rgb_color(50, 160, 255), fl_rgb_color(50, 160, 255))
        send_but.callback(self.send)


    def but_cb(self, wid):
        if wid.label() == "&Add chatter":
            client_addr = fl_input("Enter address as x.x.x.x:n").split(":")

    def listen(self):
       pass

    def send(self, wid):
        self.inp.value("")


def main():
    win = Chat()

    Fl.scheme("gtk+")
    win.show()
    Fl.run()

if __name__ == "__main__":
    main()
