#!/usr/bin/env python

from random import seed, randrange

from fltk import *

class FloodWin(Fl_Window):

    colors = ((240, 60, 60), (250, 150, 40), (240, 215, 0),
              (40, 180, 0), (45, 150, 255), (155, 90, 250))
    colors = map(lambda c: fl_rgb_color(c[0], c[1], c[2]), colors)

    def __init__(self, size, randseed=None):
        seed(randseed)

        super(FloodWin, self).__init__(size * 30, size * 24, "Floodit")
        self.color(FL_WHITE)

        self.begin()

        for y in xrange(size + 2):
            for x in xrange(size + 2):
                cell = Fl_Box(x * 20 + 10, y * 20 + 10, 20, 20)
                cell.box(FL_FLAT_BOX)
                cell.color(FloodWin.colors[randrange(6)])

        self.end()

def main():
    win = FloodWin(15, "fun")

    Fl.scheme("gtk+")
    win.show()
    Fl.run()

if __name__ == "__main__":
    main()
