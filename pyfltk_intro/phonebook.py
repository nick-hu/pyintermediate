#!/usr/bin/env python

import cPickle
from os import path

from fltk import *


def but_cb(wid, fname):
    bname = wid.label()

    if bname == "&Load":
        fname[0] = fl_file_chooser("Pick a database file", "*.txt", PATH)
        if fname[0]:
            with open(fname[0]) as data:
                try:
                    tbook.update(cPickle.load(data))
                except:
                    tbook.clear()

    elif tbook:
        if bname == "&Save as":
            sname = fl_input("Save to file:", fname[0])
            if sname:
                with open(sname, "w") as data:
                    cPickle.dump(tbook, data)
        elif bname == "&Add/Edit":
            name = fl_input("Enter name to add/edit:", brow.text(brow.value()))
            if not name:
                return
            num = fl_input("Enter number:")
            if name and num:
                tbook[name] = num
        elif bname == "&Remove":
            name = fl_input("Enter name to remove:", brow.text(brow.value()))
            if name:
                del tbook[name]

    brow.clear()
    numval.value("")
    for name in tbook.keys():
        brow.add(name)


def get_num(wid):
    if wid.value():
        numval.value(tbook[brow.text(brow.value())])

tbook = {}
PATH, fname = path.dirname(path.abspath(__file__)), [""]
col = fl_rgb_color

win = Fl_Window(200, 200, 500, 500, "Phone Book")
win.color(FL_WHITE)

win.begin()

but_labels = ["&Load", "&Save as", "&Add/Edit", "&Remove"]
but_colors = [col(80, 190, 50), col(250, 210, 65), col(50, 160, 255),
              col(255, 50, 50)]
for x in xrange(4):
    but = Fl_Button(10 + 121 * x, 10, 115, 30, but_labels.pop(0))
    but.color(but_colors.pop(0))
    but.callback(but_cb, fname)

brow = Fl_Hold_Browser(10, 50, 480, 400)
brow.callback(get_num)
numval = Fl_Output(10, 460, 480, 30)

win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()
