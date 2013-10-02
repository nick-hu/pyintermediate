#!/usr/bin/env python

from fltk import *

w, h = 500, 500
x, y = Fl.w()/2 - w/2, Fl.h()/2 - h/2  # Get width and height of screen
win = Fl_Window(x, y, w, h, "Window title")  # Creates Fl_Window object

win.begin()  # Widgets below added to win

but = Fl_Button(10, 10, 70, 30, "OK")  # (x, y, w, h, label)
inp = Fl_Input(100, 50, 70, 30, "Type")

win.end()  # Widgets above added to win

Fl.scheme("gtk+")
win.show()
Fl.run()
