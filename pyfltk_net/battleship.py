#!/usr/bin/env python

import socket
import sys
import cPickle

from fltk import *


class BattleShip(Fl_Window):
    def __init__(self, side):
        self.colors = ((180, 225, 245), (0, 150, 215), (90, 90, 90),
                       (210, 70, 70), (70, 210, 210))
        self.colors = map(lambda rgb: fl_rgb_color(*rgb), self.colors)
        self.ships, self.shippos = [], []
        self.shipsizes, self.endp = [2, 3, 3, 4, 5], []

        text = "Client" if side == "c" else "Server"
        text = "Battleship: " + text
        super(self.__class__, self).__init__(690, 360, text)
        self.color(FL_WHITE)
        self.begin()

        self.tgrid, self.ogrid = [], []
        for y in xrange(10):
            self.tgrid.append([])
            self.ogrid.append([])
            for x in xrange(10):
                tcell = Fl_Button(x*30 + 30, y*30 + 30, 30, 30)
                tcell.box(FL_THIN_DOWN_BOX)
                tcell.color(self.colors[0])
                tcell.callback(self.send, (x, y))
                self.tgrid[-1].append(tcell)
                ocell = Fl_Button(x*30 + 360, y*30 + 30, 30, 30)
                ocell.box(FL_THIN_DOWN_BOX)
                ocell.type(FL_TOGGLE_BUTTON)
                ocell.color(self.colors[1], self.colors[2])
                ocell.callback(self.placeship, (x, y))
                self.ogrid[-1].append(ocell)

        self.end()
        self.show()

        self.side, self.wait = side, True
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if side == "c":
            self.send_addr = (sys.argv[2], int(sys.argv[3]))
        else:
            self.send_addr = ()
            self.conn.bind(("0.0.0.0", int(sys.argv[2])))
        Fl.add_fd(self.conn.fileno(), self.recv)

    def placeship(self, wid, pos):
        if (pos in self.shippos) or (not self.shipsizes):
            wid.value(not wid.value())  # Reset widget
            return
        self.endp.append(pos)

        if len(self.endp) == 2:
            for pos in self.endp:
                self.ogrid[pos[1]][pos[0]].value(0)

            ship = self.validship(*zip(*self.endp))
            if ship:
                self.ships.append(ship)
                self.shipsizes.remove(len(ship))
                self.shippos = [p for ship in self.ships for p in ship]
                for x, y in ship:
                    self.ogrid[y][x].value(1)
            self.endp = []

        if not self.shipsizes and self.side == "c":
            self.wait = False  # Begin game

    def validship(self, xpos, ypos):
        xlen, ylen = abs(xpos[1] - xpos[0]), abs(ypos[1] - ypos[0])
        if not bool(xlen) ^ bool(ylen):  # Only one must be 0
            return

        length = (xlen ^ ylen) + 1
        if length not in self.shipsizes:
            return
        if not xlen:
            spos = [(xpos[0], y) for y in xrange(min(ypos), max(ypos) + 1)]
        else:
            spos = [(x, ypos[0]) for x in xrange(min(xpos), max(xpos) + 1)]

        if all(pos not in self.shippos for pos in spos):  # Cannot overlap
            return spos

    def send(self, wid, pos):
        if self.shipsizes or self.wait:  # Not ready
            return
        if self.tgrid[pos[1]][pos[0]].color() != self.colors[0]:
            return

        self.sent_x, self.sent_y = pos
        self.conn.sendto(cPickle.dumps(pos), self.send_addr)
        self.wait = True

    def recv(self, fd):
        data, self.send_addr = self.conn.recvfrom(1024)
        d = cPickle.loads(data)

        if isinstance(d, bool):  # Update tgrid
            infocolor = self.colors[3] if d else self.colors[4]
            self.tgrid[self.sent_y][self.sent_x].color(infocolor)
            self.tgrid[self.sent_y][self.sent_x].redraw()

        elif isinstance(d, int):  # Ship sunk alert
            self.tgrid[self.sent_y][self.sent_x].color(self.colors[3])
            fl_alert("Sunk ship of length " + str(d))

        elif isinstance(d, str):  # Win alert
            self.tgrid[self.sent_y][self.sent_x].color(self.colors[3])
            fl_alert(d)

        else:
            if self.shipsizes:  # Not ready
                return

            check = bool(self.ogrid[d[1]][d[0]].value())
            infocolor = self.colors[3] if check else self.colors[4]
            self.ogrid[d[1]][d[0]].color(infocolor, infocolor)
            self.ogrid[d[1]][d[0]].redraw()

            shipstates = [self.ogrid[y][x].color() for x, y in self.shippos]
            if all(c == self.colors[3] for c in shipstates):  # Win/loss
                self.conn.sendto(cPickle.dumps("VICTORY!"), self.send_addr)
                fl_alert("DEFEAT!")
                self.wait = True
                return

            if not check:  # Miss
                self.conn.sendto(cPickle.dumps(check), self.send_addr)
            else:  # Hit
                for ship in self.ships:
                    if d in ship:
                        shiphit, lship = ship, len(ship)
                        break
                for x, y in shiphit:
                    if self.ogrid[y][x].color() != self.colors[3]:
                        self.conn.sendto(cPickle.dumps(check), self.send_addr)
                        break
                else:  # If hit all, sink!
                    self.conn.sendto(cPickle.dumps(lship), self.send_addr)
            self.wait = False


def main():
    win = BattleShip(sys.argv[1])

    Fl.scheme("gtk+")
    Fl.run()

if __name__ == "__main__":
    main()
