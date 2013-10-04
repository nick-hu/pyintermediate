#!/usr/bin/env python

import os.path
import datetime as dtime

from fltk import *

PATH = os.path.dirname(os.path.abspath(__file__))


def watch_button(wid):
    wid.deactivate()
    if wid == start:
        update_time()
        reset.deactivate()
        stop.activate()
    if wid == stop:
        Fl.remove_timeout(update_time)
        start.activate()
        reset.activate()
    if wid == reset:
        stop.deactivate()
        start.activate()
        curr_time[0] = dtime.datetime.min
        timestr = curr_time[0].time().isoformat()
        watchdial.label(timestr)
        watchdial.angle1(180)
        watchdial.redraw()


def update_time():
    curr_time[0] += dtime.timedelta(seconds=1)
    timestr = curr_time[0].time().isoformat()
    watchdial.label(timestr)
    watchdial.angle1(watchdial.angle1() + 6)
    watchdial.redraw()
    Fl.repeat_timeout(1.0, update_time)


curr_time = [dtime.datetime.min]
timestr = curr_time[0].time().isoformat()

win = Fl_Window(200, 200, 250, 350, "Stopwatch")
win.color(FL_WHITE)

win.begin()

watchimg = Fl_Box(25, 15, 200, 267)
watchimg.image(Fl_PNG_Image(PATH + "/watchface.png"))
watchdial = Fl_Dial(48, 105, 155, 155)
watchdial.color(fl_rgb_color(245, 245, 245), fl_rgb_color(255, 100, 100))
watchdial.angles(0, 360)
watchdial.angle1(180)
watchdial.label(timestr)
watchdial.labelsize(14)
watchdial.align(FL_ALIGN_CENTER)

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
