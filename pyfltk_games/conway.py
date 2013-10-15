#!/usr/bin/env python

from fltk import *


class Cell(Fl_Button):
    def __init__(self, x, y, w, h, s=None):
        Fl_Button.__init__(self, x, y, w, h, s)
        self.state = False

win = Fl_Window(200, 200, 1000, 820, "Conway's Game of Life")

win.begin()

for y in xrange(82):
    for x in xrange(82):
        but = Fl_Button(x * 10, y * 10, 10, 10)
        but.box(FL_THIN_UP_BOX)
        but.color(FL_WHITE)
        if y == 0 or y == 81 or x == 0 or x == 81:
            but.box(FL_FLAT_BOX)
            but.color(FL_BLACK)

win.end()

win.show()
Fl.run()
