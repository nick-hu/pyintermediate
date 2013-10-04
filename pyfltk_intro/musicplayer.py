#!/usr/bin/python

from sys import exit
import subprocess as subp

from fltk import *


def playmusic(wid):
    mpath = "/home/inter/music/"
    fname = fl_file_chooser("Pick a music file", "*.ogg", mpath)
    if fname is None:
        return
    ps.append(subp.Popen(["ogg123", fname]))
    wid.deactivate()
    stopbut.activate()


def stopmusic(wid):
    if ps:
        ps.pop().kill()
        playbut.activate()
        wid.deactivate()
    if wid == win:
        exit("\n\nGoodbye!")

ps = []

win = Fl_Window(200, 200, 160, 60)

win.begin()

playbut = Fl_Button(10, 10, 40, 40, "@+4>")
playbut.callback(playmusic)
stopbut = Fl_Button(110, 10, 40, 40, "@square")
stopbut.callback(stopmusic)
stopbut.deactivate()

win.end()

win.callback(stopmusic)

win.show()
Fl.scheme("gtk+")
Fl.run()
