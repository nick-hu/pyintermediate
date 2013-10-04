#!/usr/bin/env python

from fltk import *

win = Fl_Window(200, 200, 500, 500, "Phone Book")
# http://www.speedtest.net/result/3012563993.png
# http://www.speedtest.net/result/3012582871.png
win.begin()

load = Fl_Button(10, 10, 100, 30, "Load")
add = Fl_Button(120, 10, 100, 30, "Add")
rem = Fl_Button(230, 10, 100, 30, "Remove")

brow = Fl_Select_Browser(10, 50, 480, 400)
numval = Fl_Output(10, 460, 480, 30)

win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()
