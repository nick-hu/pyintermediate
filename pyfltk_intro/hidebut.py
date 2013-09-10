#!/usr/bin/env python

from fltk import *


def but1_cb(wid):
    print 'Input hidden'
    inp.hide()


def but2_cb(wid):
    print 'Input unhidden'
    inp.show()

w, h = 500, 500
x, y = Fl.w()/2 - w/2, Fl.h()/2 - h/2
win = Fl_Window(x, y, w, h, "Window title")  # Creates Fl_Window object

win.begin()  # Widgets below added to win

but1 = Fl_Button(10, 10, 70, 30, "1")  # (x, y, w, h, label)
but2 = Fl_Button(100, 10, 70, 30, "2")
inp = Fl_Input(100, 50, 70, 30, "Type")

win.end()  # Widgets above added to win

but1.callback(but1_cb)
but2.callback(but2_cb)

Fl.scheme("gtk+")
win.show()
Fl.run()
