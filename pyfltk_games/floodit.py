#!/usr/bin/env python

from random import seed, randrange, randint
from sys import argv

from fltk import *

class FloodWin(Fl_Window):

    colors = ((240, 60, 60), (250, 150, 40), (240, 215, 0),
              (40, 180, 0), (45, 150, 255), (155, 90, 250))
    colors = map(lambda c: fl_rgb_color(c[0], c[1], c[2]), colors)

    def __init__(self, size, randseed):
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
                cell.color(FloodWin.colors[randrange(6)])
                if y == 0 or y == size+1 or x == 0 or x == size+1:
                    cell.color(fl_rgb_color(50, 50, 50))
                self.cells.append(cell)

        for y in xrange(2):
            for x in xrange(3):
                cbut = Fl_Button(x*25 + h+10, y*25 + 20, 20, 20)
                cbut.box(FL_THIN_UP_BOX)
                cindex = 3*y + x
                cbut.color(FloodWin.colors[cindex], FloodWin.colors[cindex])
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

        self.cells[cell].color(FloodWin.colors[cindex])
        self.cells[cell].redraw()
        del self.check[-1]

        if len(set(c.color() for c in self.cells)) == 2:
            fl_message("You win!")
            self.deactivate()


def main():
    size = int(argv[1]) if len(argv) > 1 else 15
    size = 4 if size < 4 else size
    randseed = argv[2] if len(argv) > 2 else str(randrange(1000000))
    print "\nGrid size:", size, "\tSeed:", randseed

    win = FloodWin(size, randseed)
    Fl.scheme("gtk+")
    win.show()
    Fl.run()

if __name__ == "__main__":
    main()
