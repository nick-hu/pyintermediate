#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fltk import *
from random import randrange


def but_cb(wid):
    if wid.label() in solved:
        return

    if len(shown) == 2:  # Hide shown buttons
        for let in shown[:]:
            let.labeltype(FL_NO_LABEL)
            let.color(fl_rgb_color(190, 70, 70))
            let.redraw()
            shown.remove(let)

    if wid.labeltype() == FL_NO_LABEL:  # Reveal button
        wid.labeltype(FL_NORMAL_LABEL)
        wid.color(fl_rgb_color(70, 115, 190))
        shown.append(wid)

    if len(shown) == 2 and shown[0].label() == shown[1].label():
        solved.append(shown.pop().label())  # Simultaneously clear shown
        shown.pop()


chars = ["I", "Í", "Ì", "Ĭ", "Î", "Ǐ", "Ï", "Ĩ", "Ī",
         "Ȉ", "Ȋ", "Ị", "Ḭ", "Ɨ", "İ", "Į", "Ḯ", "ı"] * 2
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
