#!/usr/bin/env python

from fltk import *

def start_watch(wid):
    Fl.add_timeout(0.01, watch_time)

win = Fl_Window(200, 200, 250, 300, "Stopwatch")

win.begin()

watch = Fl_Box(25, 25, 200, 200, "00:00:00")
watch.box(FL_OVAL_BOX)
watch.color(fl_rgb_color(220, 220, 220))
watch.labelsize(24)

start = Fl_Button(15, 250, 75, 30, "Start")
stop = Fl_Button(160, 250, 75, 30, "Stop")
reset = Fl_Button(100, 250, 50, 30, "Reset")

win.end()

Fl.scheme("plastic")
win.show()
Fl.run()
