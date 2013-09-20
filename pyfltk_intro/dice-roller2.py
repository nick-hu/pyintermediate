#!/usr/bin/env python

from fltk import *
from random import randrange
import os.path
from time import sleep

PATH = os.path.dirname(os.path.abspath(__file__)) + "/dicepics/"


def rolldice(wid):
    for _ in xrange(10):
        total = 0
        for die in (dicebox1, dicebox2):
            roll = randrange(1, 7)
            img = Fl_PNG_Image(PATH + str(roll) + ".png")
            die.image(img)
            die.redraw()
            Fl.check()
            total = total + roll
        totalbox.label(str(total))
        sleep(0.1)

win = Fl_Window(200, 200, 270, 175, "Dice")
win.color(FL_WHITE)

win.begin()

dicebox1 = Fl_Box(10, 10, 120, 120)
dicebox2 = Fl_Box(140, 10, 120, 120)
rollbut = Fl_Button(10, 140, 50, 25, "Roll")
rollbut.shortcut(" ")
rollbut.callback(rolldice)
totalbox = Fl_Box(225, 140, 50, 25)

win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()
