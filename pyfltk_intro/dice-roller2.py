#!/usr/bin/env python

import os.path
from random import randrange
from time import sleep

from fltk import *

PATH = os.path.dirname(os.path.abspath(__file__)) + "/dicepics/"


def rolldice(wid):
    for _ in xrange(10):
        total = []
        for die in (dicebox1, dicebox2):
            total.append(randrange(1, 7))
            die.image(Fl_PNG_Image(PATH + str(total[-1]) + ".png"))
            die.redraw()
        totalbox.label(str(sum(total)))
        Fl.check()
        sleep(0.08)

win = Fl_Window(200, 200, 270, 175, "Dice Roll")
win.color(FL_WHITE)

win.begin()

dicebox1 = Fl_Box(10, 10, 120, 120)
dicebox2 = Fl_Box(140, 10, 120, 120)
rollbut = Fl_Button(10, 140, 50, 25, "Roll")
rollbut.shortcut(" ")
rollbut.tooltip("Click or press space to roll the dice")
rollbut.callback(rolldice)
totalbox = Fl_Box(225, 140, 50, 25)

win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()
