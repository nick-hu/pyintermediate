#!/usr/bin/env python

from fltk import *


def but_cb(wid):
    lab_clicked.value(lab_clicked.value() + wid.label())
    sum_clicked.value(str(int(sum_clicked.value()) + int(wid.label())))

win = Fl_Window(320, 320, 320, 320)

win.begin()

x, y = 0, 0
for num in xrange(1, 10):
    but = Fl_Button(40 + 40*(x % 3), 40 + 40*y, 40, 40, str(num))
    but.callback(but_cb)
    x, y = x + 1, y + 1 if num % 3 == 0 else y

lab_clicked = Fl_Output(160, 160, 120, 40)
sum_clicked = Fl_Output(160, 200, 120, 40)
sum_clicked.value("0")

win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()
