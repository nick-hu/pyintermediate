#!/usr/bin/env python

from fltk import *


def but_up_cb(wid):
    win2.resize(win2.x(), win2.y() - 10, win2.w(), win2.h())
    win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")


def but_down_cb(wid):
    win2.resize(win2.x(), win2.y() + 10, win2.w(), win2.h())
    win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")


def but_left_cb(wid):
    win2.resize(win2.x() - 10, win2.y(), win2.w(), win2.h())
    win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")


def but_right_cb(wid):
    win2.resize(win2.x() + 10, win2.y(), win2.w(), win2.h())
    win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")


def but_hide_cb(wid):
    global hidden

    if hidden:
        win2.show()
        hidden = False
    else:
        win2.hide()
        hidden = True


hidden = True

win = Fl_Window(200, 200, 80, 80)

win.begin()

but_up = Fl_Button(30, 10, 20, 20, "&W")
but_down = Fl_Button(30, 50, 20, 20, "&S")
but_left = Fl_Button(10, 30, 20, 20, "&A")
but_right = Fl_Button(50, 30, 20, 20, "&D")
but_hide = Fl_Button(30, 30, 20, 20, "&H")

win.end()

but_up.callback(but_up_cb)
but_down.callback(but_down_cb)
but_left.callback(but_left_cb)
but_right.callback(but_right_cb)
but_hide.callback(but_hide_cb)

win2 = Fl_Window(500, 500, 200, 200)
win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")

Fl.scheme("gtk+")
win2.show()
win.show()
Fl.run()
