#!/usr/bin/env python

from random import seed, randrange
from argparse import ArgumentParser

from fltk import *

import themes


class FloodWin(Fl_Window):

    def __init__(self, size, randseed, theme):
        self.colors = themes.themes[theme]
        self.colors = map(lambda rgb: fl_rgb_color(*rgb), self.colors)
        seed(randseed)

        self.size, h = size, (size+2) * 20
        super(FloodWin, self).__init__(h + 90, h, "Floodit")
        self.color(FL_WHITE)

        self.cells, self.check = [], []

        self.begin()

        for y in xrange(size + 2):
            for x in xrange(size + 2):
                cell = Fl_Box(x * 20, y * 20, 20, 20)
                cell.box(FL_FLAT_BOX)
                cell.color(self.colors[randrange(6)])
                if y == 0 or y == size+1 or x == 0 or x == size+1:
                    cell.color(fl_rgb_color(50, 50, 50))
                self.cells.append(cell)

        for y in xrange(2):
            for x in xrange(3):
                cbut = Fl_Button(x*25 + h+10, y*25 + 20, 20, 20)
                cbut.box(FL_THIN_UP_BOX)
                cindex = 3*y + x
                cbut.color(self.colors[cindex], self.colors[cindex])
                cbut.callback(self.flood, cindex)

        self.moves = Fl_Output(h+10, h-40, 70, 20)
        self.moves.value("0")

        self.end()

    def flood(self, wid, cindex, cell=None):
        if not self.active():
            return
        if cell is None:
            cell = self.size + 3
            if wid.color() == self.cells[cell].color():
                return
            self.moves.value(str(int(self.moves.value()) + 1))
        self.check.append(cell)

        newpos = (cell-1, cell+1, cell-self.size-2, cell+self.size+2)
        for pos in newpos:
            if pos not in self.check:
                if self.cells[pos].color() == self.cells[cell].color():
                    self.flood(wid, cindex, pos)

        self.cells[cell].color(self.colors[cindex])
        self.cells[cell].redraw()
        del self.check[-1]

        if len(set(c.color() for c in self.cells)) == 2:
            self.deactivate()
            fl_message("You won in " + self.moves.value() + " moves!")


def main():
    parser = ArgumentParser()
    parser.add_argument("-size", default=15, type=int)
    parser.add_argument("-gridseed", default=str(randrange(1000000)),
                        help="seed to be used in grid generation")
    parser.add_argument("-theme", default="rainbow",
                        choices=themes.themes.keys())
    args = parser.parse_args()
    args.size = 4 if args.size < 4 else args.size

    print "\nGrid size:", args.size, "\tSeed:", args.gridseed, "\n"

    win = FloodWin(args.size, args.gridseed, args.theme)
    Fl.scheme("gtk+")
    win.show()
    Fl.run()

if __name__ == "__main__":
    main()
