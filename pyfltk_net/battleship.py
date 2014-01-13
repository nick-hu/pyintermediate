#!/usr/bin/env python

import socket
import sys

from fltk import *


class BattleShip(Fl_Window):


    def __init__(self, side):
        self.colors = ((35, 145, 255), (15, 75, 135), (90, 90, 90))
        self.colors = map(lambda rgb: fl_rgb_color(*rgb), self.colors)
        text = "Client" if side == "c" else "Server"
        text = "Battleship: " + text

        super(self.__class__, self).__init__(690, 360, text)
        self.color(FL_WHITE)
        self.begin()

        self.tgrid, self.ogrid = [], []
        self.ships, self.endp = [2, 3, 3, 4, 5], []
        for y in xrange(10):
            self.tgrid.append([])
            self.ogrid.append([])
            for x in xrange(10):
                tcell = Fl_Button(x*30 + 30, y*30 + 30, 30, 30)
                tcell.box(FL_THIN_DOWN_BOX)
                tcell.color(self.colors[0])
                self.tgrid[-1].append(tcell)
                ocell = Fl_Button(x*30 + 360, y*30 + 30, 30, 30)
                ocell.box(FL_THIN_DOWN_BOX)
                ocell.type(FL_TOGGLE_BUTTON)
                ocell.color(self.colors[1], self.colors[2])
                ocell.callback(self.placeship, (x, y))
                self.ogrid[-1].append(ocell)

        self.end()
        self.show()

    def placeship(self, wid, pos):
        self.endp.append(pos)

        if len(self.endp) == 2:
            if self.validship(*self.endp):
                pass
            else:
                for pos in self.endp:
                    self.ogrid[pos[1]][pos[0]].value(0)
            self.endp = []


    def validship(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        xlen, ylen = (x2 - x1), (y2 - y1)
        if not (x1 == x2 or y1 == y2):
            return
        horiz = True if x1 == x2 else False


def main():
    win = BattleShip(sys.argv[1])

    Fl.scheme("gtk+")
    Fl.run()

if __name__ == "__main__":
    main()