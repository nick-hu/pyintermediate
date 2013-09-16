#!/usr/bin/env python

from fltk import *
from random import randrange


def but_cb(wid):
    print shown, solved

    if wid.label() in solved:
        return

    if len(shown) == 2:
        print 'foo'
        for b in shown:
            b.labeltype(FL_NO_LABEL)
            b.color(fl_rgb_color(190, 70, 70))
            b.redraw()
            shown.remove(b)

    if wid.labeltype() == FL_NO_LABEL:
        wid.labeltype(FL_NORMAL_LABEL)
        wid.color(fl_rgb_color(70, 115, 190))
        shown.append(wid)
        if len(shown) == 2 and shown[0] == shown[1]:
            solved.append(shown[0].label())


chars = [chr(o) for o in xrange(ord("A"), ord("R") + 1)] * 2
shown, solved = [], []

win = Fl_Window(200, 200, 40*8, 40*8, "Grid 1 Game")
win.color(fl_rgb_color(245, 245, 245))

win.begin()

for y in xrange(6):
    for x in xrange(6):
        but = Fl_Button(40*x + 40, 40*y + 40, 40, 40)
        but.color(fl_rgb_color(190, 70, 70))
        but.label(chars.pop(randrange(len(chars))))
        but.labeltype(FL_NO_LABEL)
        but.callback(but_cb)

win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()
