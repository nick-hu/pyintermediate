#!/usr/bin/env python

import socket
import sys
import cPickle

from fltk import *


class Chat(Fl_Window):
    def __init__(self):
        super(self.__class__, self).__init__(500, 500, "SockChat Server")
        self.color(FL_WHITE)
        self.begin()

        self.disp = Fl_Multi_Browser(10, 10, 480, 440)
        self.disp.color(FL_WHITE, fl_rgb_color(200, 200, 200))
        self.inp = Fl_Input(10, 460, 400, 30)
        send_but = Fl_Return_Button(420, 460, 70, 30, "Send")
        send_but.color(fl_rgb_color(50, 160, 255), fl_rgb_color(50, 160, 255))
        send_but.callback(self.send)

        self.end()

        self.addrs = []
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn.bind(("0.0.0.0", int(sys.argv[1])))
        Fl.add_fd(self.conn.fileno(), self.recv)  # File descriptor

    def recv(self, fd):
        data, addr = self.conn.recvfrom(1024)
        if (not data) or (addr not in self.addrs):
            if not data:  # Disconnect
                self.addrs.remove(addr)
                info = "@C9@sClient disconnected from {0}:{1}"
            else:  # Connect
                self.addrs.append(addr)
                info = "@C149@sClient connected from {0}:{1}"
            self.disp.add(info.format(addr[0], addr[1]))

            for addr in self.addrs:
                ns_addrs = self.addrs[:]
                ns_addrs.remove(addr)  # Don't send client's own address
                self.conn.sendto(cPickle.dumps((ns_addrs)), addr)

        elif data:
            data = cPickle.loads(data)
            astr = "@C220[{0}:{1}] {2}".format(addr[0], addr[1], data)
            self.disp.add(astr)

    def send(self, wid):
        text = self.inp.value()
        if not text:
            return
        self.inp.value("")
        if not self.addrs:
            self.disp.add("@s@iNo clients connected!")
        else:
            self.disp.add("[localhost] " + text)
            for addr in self.addrs:
                self.conn.sendto(cPickle.dumps(text), addr)


def main():
    win = Chat()

    Fl.scheme("gtk+")
    win.show()
    Fl.run()

    win.conn.close()

if __name__ == "__main__":
    main()
