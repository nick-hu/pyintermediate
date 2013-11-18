#!/usr/bin/env python

import os.path
from random import randrange
from time import sleep

import fltk

PATH = os.path.dirname(os.path.abspath(__file__)) + "/dicepics/"


class DiceWindow(fltk.Fl_Window):
    def __init__(self, label=None):
        super(DiceWindow, self).__init__(200, 200, 270, 175, label)
        self.color(fltk.FL_WHITE)

        self.begin()

        self.dicebox1 = fltk.Fl_Box(10, 10, 120, 120)
        self.dicebox2 = fltk.Fl_Box(140, 10, 120, 120)
        self.rollbut = fltk.Fl_Button(10, 140, 50, 25, "Roll")
        self.rollbut.shortcut(" ")
        self.rollbut.tooltip("Click or press space to roll the dice")
        self.rollbut.callback(self.rolldice)
        self.totalbox = fltk.Fl_Box(225, 140, 50, 25)

        self.end()

    def rolldice(self, wid):
        for _ in xrange(10):
            total = []
            for die in (self.dicebox1, self.dicebox2):
                total.append(randrange(1, 7))
                die.image(fltk.Fl_PNG_Image(PATH + str(total[-1]) + ".png"))
                die.redraw()
            self.totalbox.label(str(sum(total)))
            fltk.Fl.check()
            sleep(0.08)


def main():
    win = DiceWindow("Dice Roll OOP!")

    fltk.Fl.scheme("gtk+")
    win.show()
    fltk.Fl.run()

if __name__ == "__main__":
    main()
