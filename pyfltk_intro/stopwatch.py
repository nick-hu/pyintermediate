#!/usr/bin/env python

import os.path
import datetime as dtime

from fltk import *

PATH = os.path.dirname(os.path.abspath(__file__))


def watch_button(wid):
    if wid == start:
        update_time()
        start.deactivate()
        stop.activate()
    if wid == stop:
        Fl.remove_timeout(update_time)
        stop.deactivate()
        start.activate()
        reset.activate()
    if wid == reset:
        curr_time[0] = dtime.datetime.min
        stop.deactivate()
        reset.deactivate()
        start.activate()
        timestr = curr_time[0].time().isoformat()
        watch.label(timestr)
        watch.redraw()


def update_time():
    curr_time[0] += dtime.timedelta(seconds=1)
    timestr = curr_time[0].time().isoformat()
    watch.label(timestr)
    watch.redraw()
    Fl.repeat_timeout(1.0, update_time)


curr_time = [dtime.datetime.min]
timestr = curr_time[0].time().isoformat()

win = Fl_Window(200, 200, 250, 350, "Stopwatch")
win.color(FL_WHITE)

win.begin()

watchimg = Fl_Box(25, 15, 200, 267)
watchimg.image(Fl_PNG_Image(PATH + "/watchface.png"))
watch = Fl_Box(25, 15, 200, 267, timestr)
#watch.box(FL_OVAL_BOX)
#watch.color(fl_rgb_color(220, 220, 220))
watch.labelsize(24)

start = Fl_Button(15, 300, 75, 30, "&Start")
start.color(fl_rgb_color(107, 148, 30))
start.callback(watch_button)
stop = Fl_Button(160, 300, 75, 30, "&Stop")
stop.color(fl_rgb_color(149, 23, 24))
stop.deactivate()
stop.callback(watch_button)
reset = Fl_Button(100, 300, 50, 30, "&Reset")
reset.deactivate()
reset.callback(watch_button)

win.end()

Fl.scheme("plastic")
win.show()
Fl.run()
