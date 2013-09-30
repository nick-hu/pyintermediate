#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess as subp

from fltk import *


def playmusic(wid):
    mpath = "/home/inter/music/"
    fname = fl_file_chooser("Pick a music file", "*.ogg", mpath)
    ps.append(subp.Popen(["ogg123", fname]))
    wid.deactivate()
    pausebut.activate()
    stopbut.activate()


def pausemusic(wid):
    pass


def stopmusic(wid):
    ps.pop().kill()
    playbut.activate()
    pausebut.deactivate()
    stopbut.deactivate()

ps = []

win = Fl_Window(200, 200, 160, 60)

win.begin()

playbut = Fl_Button(10, 10, 40, 40, "@+4>")
playbut.callback(playmusic)
pausebut = Fl_Button(60, 10, 40, 40, "@circle")
pausebut.callback(pausemusic)
pausebut.deactivate()
stopbut = Fl_Button(110, 10, 40, 40, "@square")
stopbut.callback(stopmusic)
stopbut.deactivate()

win.end()

win.show()
Fl.scheme("gtk+")
Fl.run()
