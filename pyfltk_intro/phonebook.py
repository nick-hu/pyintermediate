#!/usr/bin/env python

import cPickle
from os import path

from fltk import *


def but_cb(wid, fname):
    bname = wid.label()
    brow.clear()
    numval.value("")

    if bname == "&Load":
        fname[0] = fl_file_chooser("Pick a database file", "*.txt", PATH)
        if fname[0]:
            tbook.clear()
            try:
                with open(fname[0]) as data:
                    tbook.update(cPickle.load(data))
            except:
                brow.add("ERROR: Invalid database file")
                fname[0] = ""

    elif bname == "&Add/Edit" and fname[0]:
        name = fl_input("Enter name to add/edit:", brow.text(brow.value()))
        if name:
            num = fl_input("Enter number:")
            if num:
                tbook[name] = num
    elif bname == "&Save/New" and fname[0]:
        sname = fl_input("Save to file / Create new file:", fname[0])
        if sname:
            with open(sname, "w") as data:
                cPickle.dump(tbook, data)
    elif bname == "&Remove" and brow.value():
        del tbook[brow.text(brow.value())]

    for name in sorted(tbook.iterkeys()):
        brow.add(name)


def get_num(wid):
    if wid.value() and fname[0]:
        numval.value(tbook[brow.text(brow.value())])

tbook = {}
PATH, fname = path.dirname(path.abspath(__file__)), [" "]
col = fl_rgb_color

win = Fl_Window(200, 200, 500, 500, "Phone Book")
win.color(FL_WHITE)

win.begin()

but_labels = ["&Load", "&Save/New", "&Add/Edit", "&Remove"]
but_colors = [col(80, 190, 50), col(240, 185, 0), col(50, 160, 255),
              col(215, 55, 10)]
but_colors.extend(but_colors[::-1])

for x in xrange(4):
    but = Fl_Button(10 + 121 * x, 10, 115, 30, but_labels.pop(0))
    but.color(but_colors.pop(0), but_colors.pop(-1))
    but.callback(but_cb, fname)

brow = Fl_Hold_Browser(10, 50, 480, 400)
brow.color(FL_WHITE, col(200, 200, 200))
brow.callback(get_num)
numval = Fl_Output(10, 460, 480, 30)

win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()
